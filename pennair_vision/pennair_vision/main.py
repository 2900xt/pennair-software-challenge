import argparse
import sys
import time
from collections import deque

import cv2
import numpy as np

WINDOW = "PennAir"
DEFAULT = "PennAir 2024 App Dynamic.mp4"

# Detector parameters
KERNEL_SIZE = 7
ERROR_THRESHOLD = 2
AREA_THRESHOLD = 1e3
DILATION_SIZE = KERNEL_SIZE//2-1

F_x = 2564.3186869 # px
F_y = 2569.70273111 # px
x_o = 5 # inches
x_circle = 104.2163692827433
z_o = F_x*x_o/x_circle


def image_to_world(x_i, y_i):
    x_o = z_o * x_i / F_x
    y_o = z_o * y_i / F_y
    return (x_o, y_o)

# from plane_fit.ipynb
# add a dilation step to fix the kernel clipping on sides
def planar_threshold_contours_masked(image, kernel_size, error_threshold, area_treshold):
    # plane fit
    K = kernel_size
    threshold = error_threshold

    assert K%2==1
    r = K//2

    n = K*K

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)

    kOnes = np.ones(K, np.float64)

    # [-r, -r+1, ... 0 ... r-1, r]
    kRamp = np.arange(-r, r+1, dtype=np.float64)

    #sum(z_i) across the submatrix
    sz = cv2.sepFilter2D(gray, -1, kOnes, kOnes)
    szz = cv2.sepFilter2D(gray*gray, -1, kOnes, kOnes)

    #sum(x_i*z_i) across the submatrix
    sxz = cv2.sepFilter2D(gray, -1, kRamp, kOnes)

    #sum(z_i*y_i) across the submatrix
    syz = cv2.sepFilter2D(gray, -1, kOnes, kRamp)

    #sum(xx)=sum(yy) is independent of the image
    snn = K * np.dot(kRamp, kRamp)

    #z ~ a + bx + cy
    a = sz/n 
    b = sxz/snn
    c = syz/snn
    
    error_plane = szz - a*sz - b*sxz - c*syz
    error_plane_avg = np.sqrt(np.maximum(error_plane, 0)/n)
    mask = (error_plane_avg < threshold).astype(np.uint8)*255

    # gets rid of all "necks" by doing a 9x9 erode-then-dilate.
    # comes at the consequence of rounding corners, but worth for overall accuracy
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts_filtered = [c for c in cnts if cv2.contourArea(c) > area_treshold]

    return cnts_filtered, error_plane_avg

def postprocess_dilate_contours(cnts_filled, dilation_px):
    cnts_dilated = []
    dilation = dilation_px

    for contour in cnts_filled:

        # instead of just dilating with cv2, we're restricting the dilation to a bounding box
        # of size K//2+1 to prevent the floodfill contour from overfilling onto the grass.
        x, y, w, h = cv2.boundingRect(contour)
        offset = np.array([x - dilation, y - dilation])

        roi = np.zeros((h + 2*dilation, w + 2*dilation), np.uint8)
        cv2.drawContours(roi, [contour - offset], -1, 255, cv2.FILLED)

        minkowski = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation*2+1, dilation*2+1))
        roi = cv2.dilate(roi, minkowski)

        out, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt_edited = max(out, key=cv2.contourArea) + offset
        cnts_dilated.append(cnt_edited)

    return cnts_dilated


def detect(image):
    cnts, _ = planar_threshold_contours_masked(image, KERNEL_SIZE, ERROR_THRESHOLD,
                                             AREA_THRESHOLD)
    return postprocess_dilate_contours(cnts, DILATION_SIZE)


# --- drawing ---------------------------------------------------------------

OUTLINE, CENTER, STATUS = (255, 0, 0), (0, 0, 255), (255, 255, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX


def centroid(contour):
    """Centre of mass of a contour, or None if it has zero area."""
    m = cv2.moments(contour)
    if m["m00"] == 0:
        return None
    return int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])


def annotate(img, contours, status=None):
    """Copy of `img` with each contour outlined and its centre marked."""
    vis = img.copy()
    cv2.drawContours(vis, list(contours), -1, OUTLINE, 2, cv2.LINE_AA)
    for contour in contours:
        point = centroid(contour)
        if point is None:
            continue
        cv2.drawMarker(vis, point, CENTER, cv2.MARKER_CROSS, 16, 2, cv2.LINE_AA)

        x_i, y_i = point[0], point[1]
        x_o, y_o = image_to_world(x_i, y_i)
        
        _text(vis, f"({x_o:.1f}, {y_o:.1f}, {z_o:.1f})",
              (x_i + 12, y_i - 12), 0.5, CENTER)
    if status:
        _text(vis, status, (12, 34), 0.7, STATUS)
    return vis


def _text(img, s, origin, scale, color):
    # Black pass first, so text stays readable over bright shapes and dark
    # background alike.
    cv2.putText(img, s, origin, FONT, scale, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, s, origin, FONT, scale, color, 2, cv2.LINE_AA)



def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", nargs="?", default=DEFAULT,
                        help="video file, image file, or camera index")
    args = parser.parse_args()

    image = cv2.imread(args.input)
    if image is not None:
        run_image(args.input, image)
    else:
        run_video(args.input)


def run_image(path, image):
    contours, elapsed = time_detect(image)
    print(f"{path}: {len(contours)} shapes  {elapsed * 1000:.1f} ms")
    view(annotate(image, contours,
                  f"{len(contours)} shapes  {elapsed * 1000:.1f} ms  "
                  f"{1 / elapsed:.1f} fps"))


def time_detect(frame):
    start = time.perf_counter()
    contours = detect(frame)
    return contours, time.perf_counter() - start


def run_video(source):
    cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
    if not cap.isOpened():
        sys.exit(f"could not open video: {source}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    playing = True
    index = -1            # index of the frame currently on screen
    seek_to = None        # set when stepping backwards or restarting
    recent = deque(maxlen=30)   # detector times, for a rolling fps figure

    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    try:
        while True:
            advance = playing or seek_to is not None
            if advance:
                if seek_to is not None:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, seek_to)
                    index = seek_to - 1
                    seek_to = None
                # One frame in, one frame out -- the video is streamed, never
                # loaded whole.
                ok, frame = cap.read()
                if not ok:
                    playing = False
                    if index < 0:
                        break
                else:
                    index += 1
                    contours, elapsed = time_detect(frame)
                    recent.append(elapsed)
                    fps = len(recent) / sum(recent)
                    status = (f"frame {index + 1}/{total}  "
                              f"{len(contours)} shapes  "
                              f"{elapsed * 1000:.1f} ms  "
                              f"{fps:.1f} fps"
                              f"{'' if playing else '  [paused]'}")
                    cv2.imshow(WINDOW, annotate(frame, contours, status))

            key = cv2.waitKey(1 if playing else 30) & 0xFF
            if key in (ord("q"), 27) or closed():
                break
            elif key == ord(" "):
                playing = not playing
            elif key in (ord("n"), 83, 84):        # n / right / down arrow
                playing = False
                seek_to = index + 1
            elif key in (ord("p"), 81, 82):        # p / left / up arrow
                playing = False
                seek_to = max(index - 1, 0)
            elif key == ord("r"):
                seek_to = 0
                recent.clear()
    finally:
        cap.release()
        cv2.destroyAllWindows()


def view(image):
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.imshow(WINDOW, image)
    while True:
        key = cv2.waitKey(30) & 0xFF
        if key in (ord("q"), 27) or closed():
            break
    cv2.destroyAllWindows()


def closed():
    return cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1


if __name__ == "__main__":
    main()