# Build/run harness for the pennair_vision ROS 2 workspace.
#
# Everything runs inside the `ros2_jazzy` micromamba env, so recipes never
# assume the caller has sourced ROS themselves.

ENV        := ros2_jazzy
MAMBA      := micromamba run -n $(ENV)
SOURCE_WS  := source install/setup.bash
VIDEO      ?= PennAir 2024 App Dynamic Hard.mp4

.PHONY: build server viewer run stop clean

build:
	$(MAMBA) colcon build --symlink-install

# "ROS server": video_publisher + detector, wired up by the launch file.
server: build
	$(MAMBA) bash -c '$(SOURCE_WS) && ros2 launch pennair_vision pennair_launch.py video_path:="$(VIDEO)"'

# Custom stream viewer, standalone.
viewer: build
	$(MAMBA) bash -c '$(SOURCE_WS) && ros2 run pennair_vision viewer'

# Runs the server in the background and the viewer in the foreground.
# The server is started with setsid so its whole process group (ros2 launch
# + video_publisher + detector) can be killed together -- `micromamba run`
# does not forward signals to its children on its own.
run: build
	@trap 'if [ -n "$$SERVER_PID" ]; then kill -TERM -$$SERVER_PID 2>/dev/null; fi' EXIT INT TERM; \
	setsid $(MAMBA) bash -c '$(SOURCE_WS) && ros2 launch pennair_vision pennair_launch.py video_path:="$(VIDEO)"' \
		</dev/null >/tmp/pennair_server.log 2>&1 & \
	SERVER_PID=$$!; \
	echo "server starting (pgid $$SERVER_PID, log: /tmp/pennair_server.log)"; \
	sleep 2; \
	$(MAMBA) bash -c '$(SOURCE_WS) && ros2 run pennair_vision viewer'

clean:
	rm -rf build install log
