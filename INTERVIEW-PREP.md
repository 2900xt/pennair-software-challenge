# Penn Aerial Robotics — Interview Prep

Research compiled 2026-08-29 for Taha Rawjani. Sources are cited inline. Anything
unverified is explicitly flagged — see [Confidence Appendix](#confidence-appendix)
before you repeat a number out loud.

---

## 0. The one thing to know

**Penn AiR's design and presentation scores are internationally competitive. Their
flight/mission scores are not. That gap is the whole story of the club right now,
and it is where every good interview answer points.**

SAE Aero Design West 2025, Advanced Class ([official PDF](https://www.saeaerodesign.com/content/SAE-Aero-Design-West-2025---Advanced-Class-Results.pdf)):

| | Design | Presentation | **Mission** | Total | Rank |
|---|---|---|---|---|---|
| **Penn AiR (Eclipse)** | 40.01 | 32.01 | **0.0000** | 72.02 | 9th |
| 1st — Nanjing UAA (Raptor) | 43.07 | 36.52 | 52.64 | 127.23 | 1st |

Penn's design score was **4th best in the class** — ahead of the teams that placed
2nd and 3rd overall. They lost purely on flight.

In 2026 they won **1st Place, Design, Advanced Class** for *Zenith*
([official results PDF](https://www.saeaerodesign.com/content/2026-SAE-Aero-Design-West-Final-Results.pdf)).
They can engineer on paper at a world-class level. Turning paper into scored flight
is the open problem.

**Critically important framing note:** *8 of 13 Advanced Class teams scored 0.00
mission in 2025, including Georgia Tech, who had the single highest design score in
the class.* So this is not "you guys are bad" — it is "this is where the entire sport
is hard, and it's the highest-leverage place to invest." Say it that way. An
interview is not an audit.

---

## 1. The club at a glance

**Real domain: [pennaerial.com](https://www.pennaerial.com/)** (not pennaerialrobotics.com).
GitHub org: **[github.com/pennaerial](https://github.com/pennaerial)**.

- **Founded** 2014 by Lukas Vacek. Nearly died during COVID — membership fell to
  ~15 when the 2021 president joined.
- **Size:** [PennClubs](https://pennclubs.com/club/penn-aerial-robotics/) lists 59
  registered members; their own [team page](https://www.pennaerial.com/team/) claims
  "80+ students." Reality is probably in between, with a gap between registered and
  consistently active. PennClubs flags the club **highly competitive**.
- **Faculty advisor:** Siddharth ("Sid") Deliwala, Director of ESE Labs. External
  mentor: Valley Forge Signal Seekers RC Club (piloting).
- **Space:** resident student club of the **Detkin Lab** (ESE). Office hours in
  **Towne M81**. Flight testing at **Cross Keys Airfield, NJ**.
- **Time commitment (from their [join page](https://www.pennaerial.com/join-us/)):**
  ~**6 hrs/week** — a **2-hour build session Wednesdays 7–9pm** and a **4-hour
  session Saturdays 2–6pm**. Ramps up in the spring approaching competition.
  Operations meeting time is more flexible.

### Application mechanics

- Recruits **once a year, start of fall**. Application = **general questionnaire +
  team-specific technical challenge**.
- Fall 2026 cycle: **Priority app due Sept 5 midnight, Regular app due Sept 19
  midnight.** Office hours 7:15–9pm in Towne M81.
- **You can apply to multiple subteams** — they explicitly allow it, with a warning
  about overlapping time commitments.
- Only the **software** challenge is public (it's on GitHub). Mechanical, electrical,
  and operations challenges exist but their content isn't published anywhere I could find.

### What they say they want — verbatim

> "We are looking for a **strong willingness to learn**... You can join the team and
> learn everything from scratch if you are willing to put in the work."
> — [join page](https://www.pennaerial.com/join-us/)

> "Remember we are looking for **commitment and willingness to learn, not previous
> knowledge**." · "A large part of being on this team is **learning how to do research
> and figure things out**." — challenge `Instructions.md`

> "Be prepared to talk about your code and to explain how you arrived at your solution...
> you must fully understand how your code works because you will be asked to explain it."

That last line is the closest thing to a documented interview format. **Assume the
interview is largely a walkthrough of your challenge submission.** Know every line
of your own code cold, especially the parameter choices you'd struggle to justify.

### Leadership (from [team page](https://www.pennaerial.com/team/))

- **President:** Aidan Kuo · **VP Operations:** Tina Lee · **VP Finance:** Anjali
  Kalanidhi · **VP Sponsorships:** Tina Jin
- **Software Leads:** Yuzhi Liu (`yuzhiliu8`), Brian Wei (`brianwei15`)
- **Electrical Leads:** Jerry Zhang, Cymberly Tsai — sub-leads: In-Flight Sensors
  (Kristian Prifti), Power & Thrust Management (Jeremy Chung), Controls & Sensors
  Integration (Jerry Zhang)
- **Mechanical Leads:** Ojani Chung, Daniel Wang — sub-leads: Advanced Class (Ayan
  Bhatia), Micro Class (Connor Mundheim), Wing/Tail (Tina Jin)
- Recent alumni: Ethan Yu (`ethayu`, software lead), Xiangyu Chen (president ~2024–25)

**Underclassmen get real titles** — the DP reported Endi Guo, a *sophomore*, as
"Research Development Head." Don't assume you'd be doing grunt work.

---

## 2. What freshmen actually do

The path from applicant to real contributor is **directly traceable in git history**.
Many usernames that own public application-challenge repos appear as monorepo
committers the following year — JonKach, kevinli405, JasonL1238, belle-hsieh,
rushilp7, VincentZ-42, ryantanen, and a dozen more, at 1–20 commits each. The current
Software Lead (`yuzhiliu8`, 560 commits) owns a `pennair-application` repo from 2025 —
**he was an applicant one year ago.**

There is a **formal training curriculum** in the monorepo's `crash course/` directory:
`cv1.ipynb` → `pytorch_part1.ipynb` + a graded-style assignment → `digit_classification`
→ `camera_calibration.py` → `ros_demo.md` (a ROS 2 talker/listener walkthrough). So:
OpenCV, then PyTorch, then ROS 2 nodes, then camera calibration.

There's also an explicit **first-contribution ritual**, added 2026-08-28 — days before
this year's deadline. `docs/pages/tutorials/making-first-contrib.rst` walks a new
member through cloning, running the Sphinx docs locally, branching as
`user/<username>/add-contributor`, adding `docs/pages/contributors/<username>.yaml`
with `role: member`, and opening a PR. Other tutorials point new members at
`create-first-mode.rst` and `create-mission.rst` — i.e. writing actual flight modes
and missions. (Both of those files are currently the single word `TODO` — see §5.)

**Engineering practice is real:** branch-per-feature, no direct commits to main, PRs
need a reviewer, CI, `.clang-format`, Sphinx + Doxygen docs.

**Not found:** any "freshman plane" or named first-year mini-project. I looked
specifically. The crash course and the first-contrib tutorial are the real analogues.

---

## 3. Competition history — the arc

### SAE Aero Design (current focus; first entered 2024)

**2024 East (Lakeland FL) — their first, and it went badly**
([Regular PDF](https://www.saeaerodesign.com/content/2024_Aero-Design-East_Overall_Regular.pdf),
[Advanced PDF](https://www.saeaerodesign.com/content/2024_Aero-Design-East_Overall_Advanced.pdf))

| Class | Aircraft | Rank | Design | Pres. | Mission | Tech deduction | Total |
|---|---|---|---|---|---|---|---|
| Regular | Empyrean | **26/26 (last)** | 19.73 | 19.81 | 0.00 | **−5.0** | 34.54 |
| Advanced | Daedalus | 8/13 | 23.58 | 36.39 | 0.00 | 0.0 | 59.97 |

From their own [post-mortem Instagram post](https://www.instagram.com/p/C4bM-NZuMDa/):
- **Regular:** passed tech inspection Friday. Saturday scrubbed by sustained 25 mph
  crosswinds. Sunday, one attempt in ~10 mph gusts — **rotated slightly too early,
  airborne ~4 seconds, stalled from insufficient airspeed, crashed**, damaging rear
  landing gear. Repaired in 2 hours; the flight window had closed.
- **Advanced:** **both aircraft failed safety and technical inspection.** Judges
  doubted the foam structure's integrity and controllability. Neither flew.
  ⚠️ *Some secondary accounts name the second Advanced airframe "Icarus," but no primary
  source confirms it — their site lists only Daedalus. Say "both Advanced aircraft."*

**2025 West (Van Nuys CA) — the turnaround**
([Regular](https://www.saeaerodesign.com/content/SAE-Aero-Design-West-2025---Regular-Class-Results.pdf),
[Advanced](https://www.saeaerodesign.com/content/SAE-Aero-Design-West-2025---Advanced-Class-Results.pdf))

| Class | Aircraft | Rank | Design | Pres. | Mission | Total |
|---|---|---|---|---|---|---|
| Regular | Equinox | 9/26 | 37.09 | 37.30 | **21.53** | 95.93 |
| Advanced | Eclipse | 9/18 | **40.01** | 32.01 | 0.00 | 72.02 |

First scoring flight mission in club history. Last place → 9th.

**2026 West (Fort Worth TX) — first awards in three years**
- **1st Place, Design, Advanced Class — "Zenith"**
- **3rd Place, Presentation, Regular Class — "Leviathan"**
- **Tempest (Micro) placed 8th overall internationally** — built by an
  **all-freshman team of four.**
- Entered **all three classes** for the first time (Leviathan/Regular,
  Tempest/Micro, Zenith/Advanced). **9 flights, all three aircraft flew.**
  ([recap](https://www.instagram.com/p/DXfIXXygXbv/))

> ⚠️ **The 2026 results PDF publishes only top-3 per category. Penn's overall
> placements and numeric scores for 2026 Regular and Advanced are NOT public.** The only
> safely quotable 2026 facts are the two awards above and Tempest's 8th in Micro (which
> comes from their own video description, not the SAE PDF).

### The trend line — memorize this

| | 2024 East | 2025 West | 2026 West |
|---|---|---|---|
| Regular | 34.54 (last of 26) | 95.93 (9th of 26) | 3rd in Presentation |
| Advanced | 59.97 (8th of 13) | 72.02 (9th of 18) | **1st in Design** |
| Mission scores | 0 / 0 | 21.53 / 0 | 9 flights, 3 aircraft |
| Classes entered | 2 | 2 | 3 |

In 2025 Regular, Penn's design (37.09) was within ~9 points of the winner's (46.62).
Their mission (21.53) was ~60 points behind (81.42). **That is where the points are.**

### Other competitions

- **IARC 2016 (Mission 7, Atlanta):** won **Best Technical Paper**; reportedly the
  only robot in the field to attempt fully autonomous flight, beating MIT and Georgia
  Tech ([DP](https://www.thedp.com/article/2016/09/aerial-robotics-win-competition-in-august),
  [GRASP](https://www.grasp.upenn.edu/news/penn-aerial-robotics-club/)). *Not verified
  against official IARC records — the IARC site has a broken TLS cert. Single-sourced.*
  Note the verifiable award is Best Technical Paper, not an overall win; nobody solved
  Mission 7 in 2016.
- **AIAA Design/Build/Fly:** a long, rough history. 2017 is the only year with real
  flight scores (39/95, flew all three missions). 2018 (69/91) and 2019 (47/104)
  scored essentially nothing. 2024 (107/107, last) and 2025 (111/112) show submitted
  paperwork and **zero participation** — registered but never flew. ⚠️ *DBF results
  list only "University of Pennsylvania" with no team name, and Penn AiR's own site
  claims only 2018 and 2019. The 2024/2025 attribution is unverified — don't raise it.*
- **AUVSI SUAS:** **no evidence they have ever competed.** Don't mention it. (Penn
  *State* has a SUAS team — easy and embarrassing confusion.)
- **2026–27 plans:** micro-class planes, a large high-lift aircraft, a continued
  autonomous **tail-sitter VTOL** for three SAE 2027 classes, plus a **full-stack
  autonomy codebase for a quadcopter swarm for IARC** (Mission 10, "Aerial Swarm for
  Minefield Traversal" — ~1 lb vehicles directed by human gesture or voice only).
  **Note the tail-sitter is Zenith, which already flies — see §4.1.**

### The milestone they're proud of

**Oct 12, 2024, Cross Keys Airport NJ, 5 a.m.:** first successful flight test of the
largest plane in club history — >40 lb airborne, 120 ft altitude, 55 mph, successful
landing. President Xiangyu Chen: *"This is the first time it worked in the physical
world."* ([DP](https://www.thedp.com/article/2024/11/penn-air-first-successful-flight-test))

### Where they sit in the field

The SAE podium is a stable set of programs: Universidade Federal da Bahia, Nanjing
UAA, Wroclaw and Warsaw Universities of Technology, Georgia Tech, UPR-Mayagüez,
Concordia, Vellore. Penn's 2026 1st-place Advanced Design beat Vellore and Toronto;
their 2025 Advanced design score beat Wroclaw, Warsaw, and CSUN.

**Honest summary you could say out loud:** *"Strong mid-pack, fast-improving, with
top-tier engineering documentation and a maturing flight record — and now at the top
of one scored category internationally."*

---

## 4. How the aircraft actually works

### 4.1 The current fleet (SAE Aero Design West 2026)

| | **Leviathan** (Regular) | **Zenith** (Advanced) | **Tempest** (Micro) |
|---|---|---|---|
| Configuration | Fixed-wing, high-payload | **VTOL tail-sitter** | Fixed-wing, **blown lift** |
| Payload | 38+ lb | 1.5 lb | 4.6 lb (site) / 2.5 kg (video) |
| Speed | 44 mph max cruise | 51 mph max cruise | 19 mph takeoff |
| Takeoff | — | "0 ft (hover)" | 25 ft |
| Result | **3rd, Presentation** | **1st, Design** | **8th overall internationally** |

Source: [current projects page](https://www.pennaerial.com/current-upcoming-projects/) and the
[2026 results PDF](https://www.saeaerodesign.com/content/2026-SAE-Aero-Design-West-Final-Results.pdf).
Tempest's video description notes it was built by an **all-freshman team of four** — worth
knowing, since it's direct evidence that new members own real aircraft.

> **Important correction to a common assumption: Zenith is a tail-sitter, not a
> tilt-rotor, and it already exists.** Their own YouTube video *"How Not To Land A
> Tailsitter"* is described as testing "our Advanced Class aircraft, Zenith." The
> **tilt-rotor was *Eclipse* (2025)**. The tail-sitter on their 2027 roadmap is a
> *continuation*, not a new start. Getting this backwards in an interview would be bad.

**Two tensions you could raise yourself** — noticing these signals you read carefully:
- Zenith's advertised "0 ft takeoff" can't be how it scores. The 2026 rules **require a
  Conventional Takeoff**: *"Vertical takeoff from the runway is not 'conventional'... Any
  propulsion device oriented greater than ten (10) degrees from horizontal shall not be
  active during Conventional Takeoff through liftoff."* The hover is for the **DLZ
  delivery/capture**, not takeoff.
- Leviathan's 38+ lb payload under 2026 rules means a **4S 14.8 V, 2200 mAh max** pack.
  That's an aggressive energy budget — a genuinely good question to ask how they closed it.

### 4.2 Previous aircraft

**Equinox** (Regular, 2025): **15 ft wingspan, ~50 lb MTOW, up to 31 lb payload** (~62%
payload fraction), **~23.5 mph cruise**, ~100 ft takeoff, **balsa** wings and fuselage,
laser-cut and glued into ribs, spars, and stringers. Team member Avaniko Asokkumar:
*"It's our main structural material, and it's surprisingly really expensive."*

> ⚠️ Their website's "capable of lifting up to 55 lbs" is almost certainly the **rulebook
> gross-weight ceiling** (§2.13: gross takeoff weight ≤ 55 lb), **not payload.** Use
> **31 lb payload / 50 lb MTOW**.

**Eclipse** (Advanced, 2025): **30 in wingspan, ~2.7 lb** unloaded (3.50 lb limit),
**tilt-rotor VTOL**, V-22 Osprey–inspired, two electric motors on **carbon-fiber** wings
that tilt up for hover and pivot forward for cruise. Largely composite; machine vision for
payload capture. Ethan Yu, then software lead — **the single best quote to have ready:**

> *"Vertical to horizontal is pretty easy, but horizontal to vertical is a lot harder...
> You have to redirect all the forward momentum and slowly tilt the rotor so that you
> replace it with lift."*

**Empyrean / Daedalus** (2024): no published specs. ⚠️ *"Icarus"* appears in some
secondary accounts but **no primary source confirms it** — the site lists only Daedalus
for Advanced 2024. Don't assert it.

**Airfoils, high-lift devices, and gear layout are essentially unpublished.** The only hard
facts: Equinox's **sprung landing gear** and lightened tail, and Tempest being **"blown
lift"** — propwash deliberately blown over the wing/flaps to raise CLmax at very low speed,
which is exactly how you achieve a 25 ft takeoff at 19 mph. **Do not invent airfoil
designations.**

### 4.3 The avionics stack — verified from the repo

| Item | Detail |
|---|---|
| Flight controller | **Holybro Pixhawk 6C Mini** |
| Firmware | **Stock PX4 v1.17** |
| Companion | **Raspberry Pi 4B 8 GB**, Ubuntu 24.04, **ROS 2 Jazzy**, FastDDS |
| Camera | **Pi Camera Module 3**, 640×480, `plumb_bob`, via `v4l2_camera` |
| Pi ↔ FC link | **uXRCE-DDS over wired UART**, `/dev/serial0` ↔ `/dev/ttyS3` @ **921600**, on **TELEM2** |
| RC link | **Spektrum**, receiver **ORX R820X** |
| Power module | **Holybro "QAV 250"** |
| PX4 airframe | **`standard_vtol`, `SYS_AUTOSTART 4004`** |
| Payload MCU (deployed) | **Raspberry Pi + pigpio**, **SN754410** quad half-H bridge |
| Payload MCU (planned) | **ESP32-S3 + ESP-IDF v6.0.2** — stub only |
| GCS | **Tauri 2 + React 19 + Tailwind 4**, over **Foxglove WebSocket** at `ws://localhost:8765` |
| Sim | **Gazebo Harmonic**, `ros:jazzy-ros-base` CI container |
| Fleet | Pis named `air-01`, `air-02`, `payload-01`; mDNS + ed25519 SSH; Wi-Fi failover |
| Thrust stand | **HX711** load cell (10 kg), **ACS712 30A** current, **DHT11**, hall-effect RPM, BLE + PyQt5 |

**Three corrections worth internalizing:**

1. **Their PX4 and QGroundControl forks are byte-identical mirrors of upstream**
   (`ahead_by: 0` on both). **There is no custom firmware, no custom mixer, no board
   port.** Do not claim otherwise.
2. **The GCS speaks Foxglove WebSocket, not MAVLink.** No `mavlink-rs` in
   `src-tauri/Cargo.toml`; it deserializes ROS 2 CDR client-side against a
   `foxglove_bridge`. **Maturity: prototype** — a shadcn button and a hardcoded
   `/chatter` `std_msgs/String` subscription. MAVLink appears only in SITL tests.
3. **The ESP32 payload controller does not fly.** Its `main()` prints `"Hello world"`
   and the IMU driver is a self-declared stub. Real payload actuation is Pi + pigpio +
   SN754410. **This is squarely in your wheelhouse and it is an open, unclaimed job.**

**No evidence found — say "I don't know" rather than guessing:** GPS receiver model,
airspeed sensor, rangefinder/lidar, external compass, telemetry radio part number, RC
transmitter, and the **motor / ESC / propeller / battery / BEC / servo models on the
actual aircraft.** The `TMotor 2820` / `APC 10x4.7` pair in the thrust-stand README is an
**example CSV header, not measured data** — don't cite it as their hardware.

*Inference, flag it as such:* Gold sponsors are **T-Motor Hobby** (motors/props/ESCs),
**MKS** (RC servos), **Mouser**; Platinum includes **Altium** and **Cadence** (PCB design)
and **Protocase** (enclosures). A safe phrasing: *"I noticed T-Motor and MKS sponsor you —
are you flying their motors and servos?"* That's a question, not a claim.

### 4.4 The payload mechanism — the most interesting thing about this team

**The payload is a robot.** From `src/payload/README.md`: *"Payload for SAE Advanced
Class 2026: two wheel diff drive payload, front-mounted camera, rear ball caster."*

The aircraft **lands on the DLZ**, releases a servo, and a **two-wheel differential-drive
rover drives itself out from under the plane.** On a later flight it drives back for the
Capture. Config: 32 mm wheels, 121 mm track, 617 CPR encoders, 20 Hz PID loop, SN754410
H-bridge on BCM pins. Written in C++/rclcpp with a **pluginlib backend swap** —
`GPIOController` (hardware) vs `SimController` (Gazebo) — a genuinely clean sim/real
abstraction. There's even a `ComputePidZieglerNichols` service; they auto-tune the PID.

**Why this is a clever rules read** (and a great thing to compliment): §8.7.6 permits
payload **electronics** and forbids only **manual operation**. A self-driving rover is
autonomous, therefore legal — and it converts a hard *aircraft* precision-landing problem
into an easy *ground-robot* navigation problem. The plane no longer has to land on a dime,
and **Capture — worth 14 points autonomous vs. 2 manual, the highest-value segment in the
entire competition — becomes tractable** because the payload drives *itself* back.

**Critically: this is a land-and-release mission, not a ballistic drop.** There is no drop
trajectory math anywhere in their code. Getting this wrong in an interview would be obvious.

### 4.5 The vision pipeline — pure OpenCV, and it maps onto your submission

**No YOLO, no neural network anywhere in the org.** In `vehicle_common/cv/`:

- `dlz_convex_hull.py` — **HSV orange threshold** (`LOWER [5,122,125]` / `UPPER [25,255,255]`),
  Gaussian blur, corner flood-fill, 15×15 erode/dilate, convex hull, `MIN_CONTOUR_AREA = 5000`
  → finds the DLZ. *They chose orange coroplast precisely because the rulebook lets teams
  pick the color — a nice bit of design-for-perception.*
- `dlz_color_regions.py` — segments sub-regions using **combined HSV + CIELAB** discriminants.
- **`calibrate.py` / `recalibrate.py` — adaptive HSV thresholding**: binary search over
  confidence plus 20-point neighborhood refinement, **re-triggered by KL divergence between
  consecutive frame hue histograms.** ⭐ **This is your challenge Part 3 (background
  agnosticism), solved in production.** If you did anything adaptive in your own submission,
  this is the single best point of connection in the entire codebase.
- `confidence.py` — shape score = **XOR area between the contour and its `minAreaRect`**
  (rectangularity), optionally × an area prior.
- **AprilTags** `tag36h11`, 50.8 mm, four on the aircraft (front=0, back=1, left=2, right=3)
  so the *rover* can localize the *plane* for Capture.

**Pixel → world** (`tracking.py:324`) is flat-ground pinhole back-projection:
`cam_coords = inv(K) @ [x, y, 1]`, scaled by altitude, offset, then **normalized to a unit
direction vector — not a GPS fix.** So this is **closed-loop visual servoing**, not one-shot
geolocation. Wrapped in a 4-state `cv2.KalmanFilter` `[x,y,vx,vy]` that is **currently
commented out** — raw detections pass straight through.

⭐ **`K⁻¹ · [u,v,1] · Z` with a known scale is exactly the recovery you do in Part 4 with
the 10-inch circle radius.** You can speak to this from direct experience rather than
from having read their code, which is a much stronger position.

**Control:** PX4 **offboard** via `px4_msgs` — `OffboardControlMode` heartbeat +
`TrajectorySetpoint` + `VehicleCommand`. Servo fires via `VEHICLE_CMD_DO_SET_ACTUATOR`.
`PayloadDropoffMode.py` is a 4-state machine (center → land → retract → take off), gated on
`roll > 0.1 or pitch > 0.1` for stability, committing to `vehicle.land()` when lateral error
`< altitude/25` below 1 m AGL.

**Rover-side modes** are declarative YAML state machines, including
`PayloadWaitForDriveOutMode`, which waits for orange DLZ coverage ≥4% sustained **plus an
optical-flow stillness check to detect being trapped under the plane.** That is a lovely
piece of real-world defensive engineering and absolutely worth complimenting by name.

**Tail-sitter in code:** `4018 quadtailsitter` and `4020 tiltrotor` exist **only as SITL/CI
fixtures**; hardware and every SAE sim pin `4004 standard_vtol`. Transitions use
`MAV_CMD_DO_VTOL_TRANSITION`.

**No aircraft names appear anywhere in the code** — zero hits for Zenith, Leviathan,
Tempest, Equinox, Eclipse. They name things functionally (`uav_0`, `payload_0`, `air-01`).

### 4.6 The rules that drive everything

Verified directly against the [2026 rulebook PDF](https://www.saeaerodesign.com/cdsweb/gen/DownloadDocument.aspx?DocumentID=10643d37-9fd1-4821-b413-9b7ddae8724b).

**Score composition, all classes:** Technical Design Report + 2D drawing **50 pts** ·
Flight Demonstration Readiness Review presentation **50 pts** · Flight Event **unbounded**.
Both report and presentation must be submitted *and scored* to qualify for flight.
**So roughly half the score is paperwork** — which is exactly how a team wins Design and
still finishes mid-pack, and why the mission gap is where marginal effort pays most.

**Regular (2026)** — rewritten from 2025. Wingspan **72–120 in** (2025 was 120–180);
**2 or 4 motors** (2025: exactly one); battery **4S 14.8 V, ≤2200 mAh** (2025: 6S,
≥3000 mAh); **no power limiter** (2025: 750 W Neumotors); **FRP — carbon and glass —
PROHIBITED**, and the rulebook notes *"Fiber-Reinforced Plastic includes duct tape."*
**That prohibition is why they build in balsa.** Payload is **unmodified commercial 2 L
plastic bottles** carried in fully enclosed internal bays; each successful flight must
*increase* payload. Takeoff airborne within **100 ft**, land within 400 ft.

```
FFS = (FS₁ + FS₂ + FS₃)/3 + PPB
FS  = 4·(empty bottles) + 15·(filled bottles)
PPB = MAX(10 − (FS − PS)², 0)      PS = your own predicted score from the TDS
```
A filled bottle is worth **3.75×** an empty one, and the **PPB punishes you quadratically
for mispredicting your own aircraft** — it's a modeling-accuracy award. Ties broken by
lowest empty weight.

**Advanced (2026)** — *"autonomously deliver and retrieve payloads to a predefined area."*
Wingspan <120 in; **max weight 3.50 lb**; ≤3 motors; 4S ≤3000 mAh; no limiter; **no takeoff
distance limit**; **4-minute mission cap**. A Proof of Flight Video is required at
inspection — no video, no flying. Payload ≤12 in, may contain electronics **but shall not
be manually operated**. DLZ is a team-supplied **8 ft × 8 ft coroplast** sheet; no nets,
Velcro, magnets, or electronics in the DLZ. Autonomy requires a **red momentary switch the
pilot must hold** — fail-to-manual by design — and the autopilot datalink must not use the
pilot's 2.4 GHz band.

```
FFS = FS₁ + FS₂ + FS₃              (SUM of top 3, not average)
Sₓ  = 1 + (MSM × W_payload)
TB  = 2 if Tm < 120 s ; 1 if < 180 s ; 0 if < 240 s
```
| Segment | Autonomous | Manual |
|---|---|---|
| Conventional Takeoff | 2 | 1 |
| Payload Release | 4 | 1 |
| Payload Delivery | 8 | 1 |
| **Payload Capture** | **14** | **2** |
| Return To Base | 3 | 1 |

**Read the incentive out loud in an interview:** autonomous Capture is worth **7× manual**,
is the highest-value segment in the competition, and 2026 *raised* it from 12 to 14.
Because scores **sum across three flights**, reliability compounds — three mediocre
complete missions beat one brilliant one and two crashes. And since payload weight
*multiplies* every segment score on a 3.5 lb airframe, liftable payload is the direct lever.

**Micro (2026)** — no wingspan limit, but span is penalized. **450 W Neu Racing power
limiter — the only class with one.** Payload is **liquid water**, ≥67 fl oz, drained
through an external bottom port without opening the bay. **>100 ft takeoff = DQ.**

```
FS = 3 · W_payload · M  +  Z
M  = 11 / ((W_empty − 1)⁴ + 8.9)
Z  = B_takeoff − S^1.5             S = wingspan in ft
B_takeoff = 20 (≤10 ft) | 15 (10–25 ft) | 9 (25–50 ft) | 0 (50–100 ft)
```
**This is the most elegant formula in the rulebook.** Empty weight is punished to the
**fourth power**; span is taxed at `S^1.5`. So Micro is a pure payload-fraction and
short-takeoff optimization under a hard power ceiling — **which is exactly why Tempest is
blown-lift**: blown lift buys CLmax (short takeoff) without buying wingspan (taxed) or
weight (annihilated). Tempest's 25 ft takeoff → `B_takeoff = 15`.

**Universal safety rules:** gross takeoff weight ≤55 lb · 2.4 GHz RC with a fail-safe that
cuts throttle to zero on signal loss · a **removable red arming plug** in the battery
positive lead, ≥9 in from any prop, clearly visible · payload must not contribute to
structural integrity · components falling off = DQ.

> **2027 rules are not public yet.** SAE posted a LaunchPad Live event for **Sept 11, 2026**
> with 30 × $1,800 team stipends; expect the rulebook that month. This is a great thing to
> mention — it means **nobody on the team knows the 2027 Regular rules either**, and given
> how radically Regular changed from 2025 to 2026, that's a live and interesting uncertainty.

### 4.7 Why tail-sitter transition is hard

You will sound like you've done this before if you can explain it. A tail-sitter takes off
vertically on its nose, then **pitches the entire airframe ~90°** to fly as a wing. No tilt
mechanisms — the whole aircraft is the tilting element. Mechanically the simplest VTOL,
aerodynamically the nastiest:

- **Deep stall through the transition.** The wing sweeps from ~90° AoA to ~5°. Between
  roughly 15° and 60° it is fully separated — lift is nonlinear, hysteretic, and essentially
  unmodelable from steady-state polars. **You are flying through a region where your aero
  model is wrong.**
- **Control authority collapses at the worst moment.** In hover, control comes from
  propwash over the surfaces and differential thrust; in cruise, from freestream dynamic
  pressure. Mid-transition you have neither.
- **Back-transition is much harder than forward.** Forward converts thrust into airspeed —
  you gain energy. Back-transition must kill all forward momentum and replace aerodynamic
  lift with thrust in seconds, at low and decaying airspeed, pitching up through the stall.
  **This is exactly Ethan Yu's quote, and it's worse for a tail-sitter than a tilt-rotor
  because the airframe itself must rotate. It's why the video is called "How Not To Land A
  Tailsitter."**
- **Attitude singularities.** Pitching through vertical hits Euler gimbal lock. PX4 uses
  quaternions, but you're effectively tuning two controllers (MC and FW) with a blended
  handover — `VT_B_TRANS_DUR`, `VT_F_TRANS_DUR`, `VT_TRANS_MIN_TP`, `VT_B_DEC_MSS`. Get the
  blend wrong and it drops.
- **Wind sensitivity.** In hover a tail-sitter presents its **entire wing planform as a
  sail** — gusts produce large disturbance moments a quadcopter never sees.
- **Landing** must arrive at zero velocity, vertical, on small tail gear, with no wheels to
  absorb error and typically no view of the ground.

**Why choose one anyway?** Fewest actuators and least dead mass in cruise — critical under
a **3.50 lb, 3-motor** cap. A tilt-rotor spends weight on tilt servos and bearings; a
tail-sitter spends it on control software. For a team with 37 software contributors and a
hard weight limit, **that is a rational trade** — and saying so shows you understand the
design decision rather than just the failure mode.

### 4.8 The general stack, for context

```
Ground:  QGroundControl (params/tuning) ── telemetry radio ──┐
         Custom GCS (mission/status)  ── Wi-Fi/WebSocket ──┐ │
Air:     Companion (Pi 4B: ROS 2, CV, mission executive)    │ │
              ↕ uXRCE-DDS (modern) or MAVROS (legacy)       │ │
         Flight controller (Pixhawk 6C Mini, PX4) ──────────┘ │
           EKF2 · attitude & position loops · failsafes        │
              ↓                                                │
         ESCs · servos · GPS · power module ───────────────────┘
         RC receiver → manual override (always wins)
```

The load-bearing ideas, all worth being able to state:

- **Two computers, two jobs.** The FC runs hard real-time on an STM32 and must never miss a
  control deadline; the companion runs Linux where a 100 ms hiccup is survivable.
  **Never put vision on the flight controller.**
- **The FC↔companion boundary is the whole design.** Historically MAVROS (MAVLink↔ROS
  bridge). Modern PX4 offers **uXRCE-DDS**, putting the FC directly on the DDS bus as a
  first-class ROS 2 participant via `px4_msgs` — lower latency, no translation layer.
  **Penn uses the modern path.**
- **Offboard mode is a deliberate dead-man's switch.** Stream setpoints at ≥2 Hz with a
  heartbeat; stop streaming and PX4 fails over to a safe mode. (See §5.1 — their heartbeat
  runs at 10 Hz on a single-threaded executor, which is the interesting part.)
- **The safety pilot always outranks the computer** — hardware-level RC override, and SAE
  mandates the held-momentary-switch design so letting go reverts to manual.
- **Sim-first.** Gazebo + PX4 SITL running the *same* ROS 2 graph as hardware. Penn does
  this properly via the pluginlib backend swap — **more discipline than most collegiate
  teams manage, and a legitimate thing to praise.**
- **Classical CV beats deep learning here.** Fixed, known, high-contrast targets on a Pi 4
  CPU at real-time rates: HSV/LAB thresholding plus contours wins on latency, determinism,
  and debuggability. A YOLO model would be slower, need training data they don't have, and
  fail in ways nobody can diagnose on a flight line. **Their choice is correct** — and note
  your own challenge prompt explicitly recommends OpenCV over a heavier framework.

---

## 5. Weaknesses and talking points, by team

Everything in this section is **verified from their public repo, their public results,
or their own public statements.** Nothing here is invented. But read §5.0 first.

### 5.0 How to deliver any of this without torching the interview

You are a freshman applicant telling a club what's wrong with their work. The
difference between "impressive" and "insufferable" is entirely in the framing:

1. **Lead with the compliment that's actually true.** Their design scores are
   world-class. Their code has real CI, real PR review, real Sphinx docs, and a
   benchmark file where the author flagged their own methodology error. That is
   *unusually* mature for a student team. Say so, and mean it.
2. **Use "I noticed" and "I'd want to work on," never "you failed to."**
3. **Name the fix, not just the flaw.** A flaw is a critique; a flaw plus a
   one-day fix is a job application.
4. **Cite the shared difficulty.** 8 of 13 Advanced teams scored zero mission.
   Half the 2025 Regular field scored zero. You're describing the sport's hard
   part, not their incompetence.
5. **Ask before you assert.** "Is the vision pipeline still the framerate
   bottleneck on the Pi, or did the C++ migration land?" invites them to teach
   you, and shows the same knowledge, with none of the arrogance.
6. **Don't quote issue numbers like a lawyer.** One is proof you read the code.
   Five is a performance.

---

### 5.1 SOFTWARE

Their stack, verified from [`pennaerial/monorepo`](https://github.com/pennaerial/monorepo):
**ROS 2 Jazzy + a PX4 fork over uXRCE-DDS + Gazebo**, a **Raspberry Pi 4B 8GB**
companion with a **Pi Camera Module 3**, an **ESP32 payload controller**, and a
**Tauri + Vite + TypeScript** ground control station. Tree spans `controls/`,
`gcs/`, `payload_controller/`, `gz-models/`, a `PX4-Autopilot` fork, and
`Dependencies/`. 39 open issues; actively developed.

Dead repos to ignore: `pennair2`, `auwl`, `interop`, `bootcamp`, `rostest`,
`ros-setups` — last pushed 2016–2023.

**Bus factor:** `yuzhiliu8` 560 commits, `ethayu` 256, `brianwei15` 201, then a
cliff to 61, 45, 38, and a long tail of 1–20. **Three people are ~85% of the
codebase**, and one of them (`ethayu`) is already tagged `alum`.

#### The five strongest software talking points

**A. Their #1 active workstream is a Python→C++ vision migration — join it.**
Issue #169 (closed) found that *"deploying our current vision pipeline (v4l2 +
CameraNode + VisionNodes) drops framerate of streaming dramatically on PIs."*
Root causes they identified: duplicated raw+compressed streams, redundant JPEG
decompress/recompress, unconditional debug-stream compression. Their own
benchmark (`src/tools/benchmark/vision_results.md`, 7/17/2026) measured
`camera_node` at YUYV 1280×1080 burning **33.5% CPU idle, 86–96% average with
bursts to 175%** as soon as anything subscribes to the raw stream.

Issues **#357/#358/#359** are the response: migrate the pipeline to C++
composable nodes with pluginlib and zero-copy `image_transport`. **If you can
write modern ROS 2 C++, this is the single highest-demand skill they have
posted.** The relevant techniques: lazy publishing (only encode when a subscriber
exists), intra-process comms so the image is never serialized between camera and
detector, `MultiThreadedExecutor` with callback groups so vision can't starve
control, and debug streams behind a runtime-toggleable parameter.

**B. Detections are timestamped at publish time, not capture time.** In
`PayloadAprilTagNode.py:345` and `PayloadColorSquareNode.py:257`:
`msg.header.stamp = self.get_clock().now().to_msg()`. That records when the CPU
*finished processing*, not when the photon hit the sensor. Since #169 establishes
the Pi pipeline is latency-bound, every detection gets fused against a pose from
tens-to-hundreds of milliseconds in the future.

**Do the math out loud — it's the most persuasive thing you can say.** At Equinox's
published 23.5 mph cruise (~10.5 m/s), **200 ms of unmodeled latency is ~2.1 m of
position error on every single target fix.** The fix is a day of work: propagate
the source `Image.header.stamp` through the pipeline into the detection message,
then do a `tf2` buffer lookup *at that stamp* instead of taking the latest pose.

This failure mode is nasty because the error **scales with airspeed and vanishes
in hover** — so it looks like a CV problem and sends teams tuning thresholds for
weeks.

**C. There is no flight-log recording. Anywhere.** Zero hits for `rosbag`,
`ros2 bag`, or `SequentialWriter` in the entire tree. The closest thing is
`CameraNode.py:388` doing `cv2.imwrite(f"{int(time.time())}.png")` — whole-second
filename resolution, so frames within the same second overwrite each other, and
no pose recorded alongside. Combine that with issue #262 (*"the logging is very
very verbose... nav gps mode logs are pretty cooked"*).

**Why this is the highest-ROI fix in the repo:** a flight test costs a 5 a.m.
wake-up, an hour's drive to Cross Keys, and ~20 people's Saturday. An
unexplainable flight is a wasted week. The fix: **auto-start `ros2 bag` on arm**,
recording detections, poses, setpoints, and mode transitions, plus *decimated*
imagery (1–2 Hz keyframes — full-rate video will exhaust the SD card and starve
the CPU). Pull the PX4 `.ulg` after every flight. Then institute the actual
cultural half: **no new code flies until the last flight's logs have been
reviewed.** That's the mechanism that turns scarce flight time into compounding
knowledge, and it costs nothing.

**D. Open bug #272 — the failsafe fights the autopilot.** Their own words:
*"mode manager keeps trying to arm the vehicle WHILE also initiating a land mode
command, even after the vehicle is on the ground, which can probably be very bad
when doing actual flight tests."* The land command is spammed every loop
iteration, forever, with the vehicle still armed. Related: **#133** —
`failsafe_trigger` is supposed to command PX4 into RTL via `VehicleCommand` and
currently doesn't (open since Feb 2026).

The correct pattern: a failsafe should be **one-shot and latching** — send
`VEHICLE_CMD_DO_SET_MODE` to RTL/LAND *once*, set a latch, then **stop
transmitting setpoints entirely** and let PX4 own the vehicle. A companion
computer that keeps talking after handing off is one that can un-hand-off. Add a
disarm on the landed-state transition to exit the loop.

**E. SITL tests exist and don't gate anything.** A `ctsim` target exists in
`.aliasrc` but **`mergebuild.yml` only invokes `ct`** (unit tests) — so SITL
regressions merge freely. Worse, **#352** notes the nightly workflow *"opens a pr
to update submodules if the docker image builds correctly, and doesn't depend on
tests passing or not"* — meaning submodule bumps, **including their PX4 fork**,
can land untested. And `mergebuild.yml`'s path filter carries
`# TODO: add docs, payload_controller, and gcs`, so **the ESP32 firmware and the
GCS are not gated by CI at all.**

Related: **#155 "make sim like real"** — they want to artificially rate-limit the
sim camera and inject latency to match reality. They know their sim is optimistic.
Wiring `ctsim` into `mergebuild` is a small diff with outsized effect.

#### Secondary software points (hold in reserve)

- **Hardcoded, uncalibrated CV constants.** `cv/dlz_color_regions.py:26` has
  `ORANGE_LOWER = np.array([5, 78, 158])` plus ~10 more bare magic numbers
  declared *inside* the function body. `cv/threshold.py` has two alternative
  `inRange` tuples commented out — the fingerprint of field-tuning by editing
  source. `PayloadDriveOutNode.py:39` says `# TODO: tune this threshold based on
  real camera output.` **None of it is a ROS parameter**, so retuning at the field
  means editing Python and rebuilding — on a laptop, in the sun, at 6 a.m. Fix:
  move every threshold to a ROS 2 parameter with a `SetParametersCallback` so it's
  live-tunable from the GCS. This is a genuinely great first PR.
- **Camera calibration is unused and mismatched.**
  `config/camera_calibrations/camera_info_0.yaml` is a **640×480** calibration
  with meaningful distortion (k1 = 0.2177, k2 = −0.3147) — but there's **no
  `undistort` / `initUndistortRectifyMap` / `projectPixelTo3dRay` call anywhere in
  the vision path.** `CameraInfo` is subscribed and stored (`base/vision_node.py:231`)
  and passed around, but pixel→bearing math appears to run on raw distorted pixels.
  Meanwhile the benchmark ran the camera at **1280×1080** — intrinsics scale with
  resolution, so the calibration is simply wrong for the stream. With k1 ≈ 0.22 the
  corner-of-frame radial error is several percent of image width, which at altitude
  is meters on the ground — and edge detections are the majority when you're
  sweeping a search pattern.
- **Single-threaded executors everywhere.** All 14 node entrypoints use
  `rclpy.spin(node)` — no `MultiThreadedExecutor`, no callback groups. The PX4
  offboard heartbeat is published from `ModeManager.spin_once` on a
  `create_timer(0.1, ...)` — **10 Hz**. PX4 requires ≥2 Hz proof-of-life and fires
  the offboard-loss failsafe after `COM_OF_LOSS_T`
  ([PX4 docs](https://docs.px4.io/main/en/flight_modes/offboard.html)). At 10 Hz on
  a single-threaded rclpy executor on a Pi 4, **five consecutive missed callbacks
  drops you out of offboard** — and the symptom is the aircraft randomly reverting
  to loiter mid-mission with *nothing* in the ROS logs, because the evidence is in
  the PX4 `.ulg`. Fix: dedicated node or callback group at 20–50 Hz.
  **Give credit where due:** they got the hard part right — `vehicle_common/mode.py:52`
  `send_request()` is properly non-blocking (`call_async` + poll `future.done()`),
  so vision calls don't stall the loop. But `mode_manager.py:139`
  `_connect_vision_client` is a `while True` with a 1 s `wait_for_service`, **no
  timeout and no failure path** — if a vision node dies or is misnamed, the mode
  manager hangs forever.
- **#253 — the `NavGPS` "LOCAL" coordinate frame is ambiguous.** PX4 is NED, ROS
  is ENU, their frame is named neither. A classic sign-error crash waiting to happen.
- **Payload actuation is stubbed in the mission state machine.**
  `PayloadDropoffMode.py:65` has `if True:  # TODO: Check if payload is dropped off
  (servo is fully retracted)` and `PayloadPickupMode.py:69` has `pass  # TODO:
  Extend servo`.
- **Onboarding is broken right now** (#397/#401): hardcoded paths from one member's
  machine in the ESP-IDF `eim` `.toml`, and the `ci/ci.conf` apt step fails. The two
  tutorial docs pages (`create-mission.rst`, `create-first-mode.rst`) are literally
  the single word `TODO` (#384/#385). **Fixing new-member setup is a trivially
  winnable, immediately visible first contribution** — and it's the kind of thing a
  team with a documented knowledge-transfer problem will actually value.
- **#167 "Unslopify monorepo"** — they know there's LLM-generated cruft in the tree.
  Signals they care about code quality. Don't bring this one up; it's a bit pointed.

> 🔒 **Handle privately, if at all:** `scripts/hardware/provision-pi.sh` contains
> `TRAVEL_ROUTER_PSK="${TRAVEL_ROUTER_PSK:-pennair123!}"` — their competition-travel
> WiFi password, committed in plaintext to a public repo. This is a real finding and
> worth reporting, but **not as an interview flex.** Mention it quietly to a software
> lead after you're in, or in a private message — never in a room, never as a gotcha.

---

### 5.2 ELECTRICAL

Their electrical subteam is explicitly described as: testing and debugging
electrical systems; integrating sensors, avionics, and onboard electronics; and
**embedded firmware for real-time control and communication**
([join page](https://www.pennaerial.com/join-us/)). Sub-teams are In-Flight
Sensors, Power & Thrust Management, and Controls & Sensors Integration.

**This is the closest match to your day job.** Blue Vigil firmware, on drones,
professionally. Lead with that.

⭐ **The single most concrete opening on this team:** their **ESP32-S3 payload controller
is a stub** — `main()` prints `"Hello world"` and the IMU driver is a self-declared
placeholder. Real payload actuation currently runs on a Raspberry Pi with pigpio and an
SN754410 H-bridge. So there is a **real, scoped, unclaimed embedded firmware job sitting
in their repo**, on the exact subsystem that feeds the 14-point autonomous Capture — as
close to a perfect match for a professional firmware engineer as a club application gets.
Phrase it as interest, not audit: *"I saw the ESP32 payload controller is still
scaffolding while the deployed path is Pi + pigpio — is moving actuation onto the ESP32
still on the roadmap? That's the kind of thing I do at work."*

Verified hardware hooks: **ESP32 payload controller** (in `payload_controller/`,
ESP-IDF toolchain), **Raspberry Pi 4B** companion, **PX4** flight stack, and a
[`PennAirThrustStand`](https://github.com/pennaerial) repo — so they already
instrument propulsion.

The failure modes worth being able to discuss (**general UAS engineering knowledge,
not verified Penn-specific findings** — frame these as "things I'd want to check,"
not "problems you have"):

- **Connector and solder-joint vibration failure.** Airframes vibrate at motor and
  prop-pass frequency; unsupported wire mass at a solder joint is a cantilever
  fatiguing at that frequency. *Symptom:* intermittent sensor dropouts that
  correlate with throttle and are unreproducible on the bench. *Fix:* strain-relieve
  every connector, adhesive-lined heatshrink, service loops, harnesses zip-tied to
  structure, locking connectors (JST-GH with retention, not friction-fit DuPont) on
  anything flight-critical, and **pull-test every connector as a preflight item.**
- **Servo inrush brownouts.** Multiple servos stalling at once — e.g. a VTOL
  transition tilting rotors under aero load — can pull tens of amps for tens of
  milliseconds. *Symptom:* the flight controller reboots mid-maneuver, which looks
  exactly like a software crash and **gets misdiagnosed as one.** *Fix:* size the
  BEC to **stall** current not rated current, bulk electrolytic capacitance at the
  servo rail, separate the servo rail from the FC/companion rail, and **log rail
  voltage** so a brownout is visible in the log rather than inferred. Directly
  relevant to their tail-sitter VTOL plans.
- **EMI from ESCs into GPS/compass.** Compass error scales linearly with current
  draw ([ArduPilot's guidance](https://ardupilot.org/copter/docs/common-magnetic-interference.html)
  applies equally to PX4 airframes). *Symptom:* heading drifts with throttle,
  toilet-bowling, EKF yaw innovations spiking under load, satellite count dropping
  at high throttle. *Fix:* short and **twisted** battery→PDB→ESC runs, 4-in-1 ESCs,
  external compass on a mast, foil-shielded USB3/HDMI harnesses, and re-run
  CompassMot after any harness change.
- **Battery C-rate and voltage sag.** *Symptom:* a pack reading 15.0 V static
  collapsing to 13.2 V under takeoff current and tripping a low-voltage failsafe
  mid-climb; or endurance at 60% of the spreadsheet. *Fix:* size on **measured**
  sag under load, log per-cell voltage, set failsafes on consumed mAh or
  sag-compensated voltage rather than instantaneous volts, and cycle-count/retire packs.
- **No fusing, no single-point-of-failure analysis.** *Fix:* a fused or
  current-limited main battery lead, and an actual **FMEA table** — for every
  component, what happens when it fails and what the mitigation is. **Judges reward
  this and it's genuinely load-bearing for safety** — which matters a lot to a team
  whose Advanced entries once failed tech inspection outright.
- **Telemetry range and antenna placement.** *Symptom:* link drops when the aircraft
  banks away. *Fix:* antennas vertical and clear of **carbon fiber, which is
  conductive and shadows RF** — a big one for Penn, who are explicitly building
  carbon airframes. Diversity antennas on the ground station, ground antenna on a
  mast, and a link-budget check before assuming coverage of the whole search box.
- **⭐ No hardware-in-the-loop bench.** A permanently powered rig with the real
  flight controller, real companion computer, real camera, and real servos, props
  off. **This is the single highest-leverage physical artifact a student team can
  own, and it's cheap** — it converts "we need a flight test" into "we need twenty
  minutes," which is the actual bottleneck on everything (see §5.3). They already
  have a thrust stand, so the instinct is there. **If you want one flagship
  electrical pitch, this is it.**

---

### 5.3 OPERATIONS

Operations does project management across subteams, sponsor and external marketing,
socials, and community outreach. It's the least technical-sounding team and the one
where a technical person can make the most visible difference — because **every
technical problem above is downstream of an operations constraint.**

**The core insight to lead with: flight-test cadence is the binding constraint on
the entire club.** Cross Keys NJ, 5 a.m. call, ~20 students, an hour each way,
weather-dependent, safety-pilot-dependent. Every hour of air time is enormously
expensive. Almost every technical fix worth making is really a way to **buy more
information per flight** or **need fewer flights.**

Verified operational pain points:

- **Self-diagnosed knowledge-transfer failure.** [Penn Today](https://penntoday.upenn.edu/news/flying-high-penn-aerial-robotics-club-will-take-part-international-competition):
  membership fell to ~15 post-COVID and **"Leadership departed without transferring
  institutional knowledge."** The rebuild explicitly prioritized documenting designs,
  coding practices, and lessons learned. **This is their own diagnosis of their own
  problem — so raising documentation and onboarding is agreeing with them, not
  correcting them.** It's the safest critique in this entire document.
  - And yet: **I found no public retrospective, post-mortem, or lessons-learned
    artifact anywhere** — not on the site, not in the repo, not in the docs. The
    stated priority hasn't produced a durable artifact. Meanwhile the bus factor is
    3 people at 85% of the code, and the onboarding path is currently broken.
    *That's a clean, specific, generous pitch: "you said this mattered; I'd like to
    build the thing that makes it stick."*
- **Schedule pressure**, in their own words: *"We're kind of just racing against
  time, right?"*
- **Travel logistics** — Penn Today names moving the 15-ft, 50-lb Equinox to LA as
  their top competition worry. *Fix:* design for **transport** from day one
  (removable wing panels, a shipping case designed alongside the airframe), do a
  timed disassemble/reassemble dry run, and carry flight-critical electronics as
  hand baggage.
- **Tech inspection prep.** They lost an entire competition to this in 2024 — both
  Advanced aircraft failed inspection and never flew, and Regular took a −5.0
  deduction. *Fix:* read the rulebook **as a checklist**, self-inspect a month out,
  pre-build the required documentation, and verify weight and CG **on a scale, not
  in CAD.*
- **Budget/sponsorship** — they run a GoFundMe. *Fix:* an itemized budget tied to
  the technical plan, sponsor deliverables treated as real obligations, and a
  corporate-relations owner who isn't also the chief engineer.

Process fixes that are pure operations and cost nothing:

- **A written test card for every flight** — the specific hypotheses this flight
  will settle, the exact data needed to settle them, and a fixed order of test
  points. Rehearse setup, checklist, and comms on the ground first.
- **Preflight checklist discipline** — physical printed checklist, read aloud, two
  people, challenge-and-response, *every* flight including the ones you're sure
  about. Control-surface direction check is the single highest-value item; add a
  "config diff vs. last known-good." Reversed surfaces after a servo swap, a prop on
  backwards, and a half-charged pack are the classic ways to lose an airframe.
  **Note their 2024 Regular crash was an early rotation into a stall — exactly the
  class of event a disciplined test card and briefed abort criteria address.**
- **A standing post-flight log review** before any new code flies (pairs with §5.1C).
- **Spares kit that travels** — servos, ESCs, props, connectors, wire, a spare
  flight controller and companion computer, pre-flashed SD cards. A $4 part should
  never end a test day; they lost their 2024 Regular flight window to a 2-hour repair.
- **FAA Part 107 / airspace.** ≤400 ft AGL, visual line of sight, daylight;
  BVLOS needs a waiver. Autonomous search patterns are exactly the operations that
  need attention. Have Part 107-certificated members, a designated visual observer,
  and LAANC-checked airspace per site — the RC field may sit under controlled
  airspace. **Note the 400 ft ceiling directly caps your ground sample distance**,
  which loops straight back into whether the vision pipeline can see the target at all.

---

## 6. Defending your challenge submission

The one documented interview expectation is *"be prepared to talk about your code
and explain how you arrived at your solution."* Your submission is the 5-part shape
detection challenge (static → video → background-agnostic → 3D → ROS 2), which maps
almost perfectly onto their real vision pipeline. Expect the interview to probe
exactly the places where a naive solution is brittle.

**Anticipate these questions and have real answers:**

| Likely question | What they're really testing | Strong answer direction |
|---|---|---|
| "Why those HSV thresholds?" | Whether you tuned by eye and stopped | You didn't threshold in HSV at all for Part 3, or you did and can say why it's insufficient — auto-white-balance chasing a mostly-green field moves the reference frame under your bounds. Better: CIELAB a\*/b\* or normalized rg-chromaticity, which decorrelate chroma from luminance far better. |
| "How does this handle a background it's never seen?" | Part 3, the real discriminator | Background-agnostic means *not* modeling the background's color. Edge/texture-based segmentation, adaptive thresholding, or a "shapes are locally uniform, grass is high-frequency" argument. Then a **geometry gate** — contour area, extent, solidity, aspect ratio — so a beige dirt patch can't pass a color gate. |
| "What's your frame rate, and where does it go?" | Efficiency is a graded criterion, and their #1 real problem | Know your actual per-frame budget and which op dominates. Bonus: mention avoiding redundant color-space conversions and per-frame reallocations. |
| "How would this behave on a real aircraft at 25 mph?" | Whether you think about the system, not the exercise | Motion blur, rolling shutter, GSD, latency (see below). This is where you can be memorably better than other applicants. |
| "How did you get depth from a single camera?" | Part 4 | Known circle radius (10 in) + focal length: Z = f·R_real / r_pixels, then X = (u−c_x)·Z/f_x, Y = (v−c_y)·Z/f_y. **Note the provided K has c_x = c_y = 0**, which is physically odd — say so; noticing it is a point in your favor. |
| "What breaks first?" | Engineering maturity | Have a real answer. Everyone says "nothing." |

**Four systems concepts that will make you sound like you've done this before** —
and all four connect directly to §5.1:

1. **Motion blur budget.** Ground smear = groundspeed × exposure time. At 10 m/s
   with a 1/100 s exposure, that's **10 cm of smear.** The mapping rule of thumb is
   to keep smear below one-third of GSD. Penn's Equinox cruises at 23.5 mph ≈ 10.5
   m/s, so this is live for them. Fix: shutter-priority with a hard exposure ceiling
   derived from cruise speed, buy the light back with gain, denoise. And **lock the
   camera** — fixed exposure, gain, and white balance. Auto-anything is a moving
   reference frame under your thresholds.
2. **GSD math nobody does.** GSD ≈ (altitude × sensor_width) / (focal_length ×
   image_width). Teams pick altitude for flight safety and camera settings
   separately, and never multiply them together. Symptom: *"we can see it on the
   debug stream but the detector never fires"* — the target is 6 px across and every
   morphological op has a minimum-area filter above that. Do the arithmetic
   **before** choosing search altitude: write down the minimum pixel count your
   detector needs (typically ≥20–30 px on the smallest feature), invert for max
   altitude, make it a documented mission constraint. **It's free points in a design
   report**, which is a language Penn speaks fluently.
3. **Temporal consistency over per-frame confidence.** Require N-of-M consistency
   before a detection promotes to an action, and cluster detections in **world
   frame, not image frame** — a real target accumulates hits at one lat/lon across
   many frames and viewing angles; clutter doesn't. Set the action threshold well
   above the detection threshold.
4. **Timestamp at capture, not at publish.** See §5.1B. If you built this into your
   own submission, you can say "I hit this in my own pipeline" rather than "I noticed
   you have this bug" — **which is a dramatically better way to raise it.**

---

## 7. Your angle

Your background is unusually well-matched, and in a way most applicants aren't. Use it.

**Firmware engineer at [Blue Vigil](https://www.bluevigil.com/) — construction
drones. Professionally. On UAVs.** This is the single strongest card in your hand
and it's not close. Most freshman applicants have coursework; you have shipped
firmware on flying hardware. It maps directly onto their Electrical subteam's
"embedded firmware for real-time control and communication" and onto the ESP32
payload controller. It also gives you standing to talk about brownouts, EMI,
harness discipline, and HIL benches as things you've *dealt with*, not read about.

**Map the rest:**

- **6502 breadboard computer, built and programmed in assembly** → you debug at the
  hardware/software boundary, which is exactly where a companion-computer-plus-flight-
  controller system fails. Also just a memorable story.
- **neo-OS** → schedulers, interrupts, real-time constraints. Directly applicable to
  "why does the offboard heartbeat miss deadlines on a single-threaded executor."
- **Whale-tracking buoys, ISEF, presented at OSM** → you've built a full
  sensing-and-telemetry system that had to survive a real, hostile environment and
  you presented it to judges. **That's the SAE design-report-and-presentation skill
  set**, which is the half Penn is already elite at. Also, it's field-deployed
  embedded work — the operational-discipline lessons transfer.
- **Competitive programming (Codeforces)** → the algorithmic half of the challenge,
  and credible speed under time pressure.
- **This repo** → you've now actually done their software challenge. Be ready to
  discuss it end to end.

**Which team(s) to apply to.** You can apply to multiple — they allow it explicitly,
with a time-commitment caveat. Given your profile:

- **Electrical** is arguably your strongest differentiator — a firmware engineer with
  professional drone experience applying to a subteam whose charter literally says
  "embedded firmware for real-time control and communication."
- **Software** is where the most public, most legible problems are, and where your CV
  challenge submission speaks for itself. Their live C++ vision migration is a
  concrete on-ramp.
- **Operations** would be an odd primary for you, but if you do apply, the pitch is
  *technical* operations: flight-test throughput, logging discipline, knowledge
  transfer. Not marketing.

If you apply to two, be ready for "which is your first choice?" and have a real answer.

**A three-sentence version of your pitch, to adapt:**

> "I write firmware for construction drones at Blue Vigil, so I've spent a lot of
> time on the part where the flight controller and the companion computer have to
> agree with each other. What drew me to Penn AiR is that your design scores are
> already top-of-field — the 2026 Advanced Design win, the 40.01 in 2025 — so the
> interesting problem isn't the design, it's converting it into scored flight. I'd
> want to work on the infrastructure that makes each 5 a.m. flight test actually
> yield answers."

### Questions to ask them

Good questions here double as evidence you did the work, and they're safer than
assertions:

- "Is the vision pipeline still the framerate bottleneck on the Pi, or has the C++
  composable-node migration landed?"
- "How do you currently review what happened on a flight test — is there bag
  recording, or is it mostly the PX4 logs?"
- "How much of the autonomy stack gets exercised in SITL before it goes to Cross
  Keys?"
- "The Advanced class mission score has been the hard part for basically everyone —
  what do you think the binding constraint is for you specifically? Airframe
  reliability, autonomy, or flight-test hours?"
- "What's the plan for the tail-sitter transition? That seems like the hardest thing
  on the 2027 roadmap." (Their former software VP: *"Horizontal to vertical is a lot
  harder."*)
- "How do you handle handoff when the three or four people who know the codebase
  graduate?"
- "What does a new software member actually own by the spring?"

### Things NOT to say

- Don't quote a **2026 overall placement or score** — it isn't public.
- Don't mention **AUVSI SUAS**. No evidence they've competed; you'd be thinking of
  Penn State.
- Don't raise the **DBF 2024/2025 last-place finishes** — the attribution to Penn AiR
  is unverified, and it's a purely negative thing to bring up regardless.
- Don't say they "won IARC 2016." The verifiable award is **Best Technical Paper**.
- Don't raise the **committed WiFi password** in a room. See the note in §5.1.
- Don't lead with a list of their bugs. One well-chosen observation, framed as
  something you want to work on, beats five framed as findings.

---

## 8. Confidence appendix

**Verified from primary sources** (official SAE results PDFs downloaded and
text-extracted, their own website, their public GitHub, DP/Penn Today articles):
all SAE placements and scores for 2024 and 2025; the 2026 Design and Presentation
awards; the 2024 post-mortem details; all quoted issue text and file/line references
in the monorepo; application deadlines and time commitment; subteam charters;
leadership names; the Oct 2024 flight test details.

**Explicitly NOT verified — do not assert these:**

- Penn's **overall placement or numeric scores at SAE 2026** — only top-3-per-category
  is public; the rest is behind SAE STARS.
- Whether the **DBF 2024/2025 "University of Pennsylvania" entries are Penn AiR.**
- **IARC 2016** Best Technical Paper — single-sourced to the DP; the official IARC
  site has a broken TLS certificate and couldn't be checked. IARC 2019 Mission 8
  result: not found.
- Any Penn presence at **2022 SAE Aero Design West** (results only behind
  inaccessible Adobe review links).
- Whether there is a **formal interview round** at all, how many rounds, or the
  acceptance rate. The documented pipeline is questionnaire + challenge, plus the
  instruction to be ready to explain your code.
- The content of the **mechanical, electrical, and operations challenges** — not
  public anywhere.
- **Team size** — the 59 vs. 80+ discrepancy is unresolved.
- Whether Wednesday/Saturday build sessions are in Detkin, Towne, or elsewhere.
- **The motor, ESC, propeller, battery, BEC, and payload servo actually flown**, plus GPS
  receiver, airspeed sensor, rangefinder, external compass, telemetry radio, and RC
  transmitter models. The `TMotor 2820` / `APC 10x4.7` in the thrust-stand README is an
  **example CSV header, not their hardware.** The T-Motor/MKS sponsorship mapping is
  inference — ask, don't assert.
- The name **"Icarus"** for the second 2024 Advanced airframe.
- **Airfoil designations, flap types, and landing gear layouts** — almost entirely
  unpublished. Don't invent them.
- **IARC Mission 10 details** (prize, dates, vehicle mass) — from search results only; the
  official IARC site couldn't be fetched.

**General engineering knowledge, not Penn-specific findings** — everything in §5.2
(electrical failure modes), the process recommendations in §5.3, and the systems
concepts in §6. These are real and worth knowing, but frame them as "things I'd want
to check," never as "problems you have."

**One caution on staleness:** the monorepo is actively developed and issues get
closed. Anything cited here from GitHub was true as of the research date at the top
of this file. **Re-check the issue tracker the day before your interview** — nothing
is worse than confidently describing a bug they fixed last week.
