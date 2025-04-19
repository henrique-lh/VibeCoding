from manim import *
import numpy as np

class ConcentricOrbitSpheres(Scene):
    def construct(self):
        num_spheres = 7
        min_radius = 0.8
        max_radius = 3.2
        linear_speed = 1.2  # constant for all
        duration = 10       # total animation time

        # Create radii linearly spaced
        radii = np.linspace(min_radius, max_radius, num_spheres)

        # Center of all circles
        center = ORIGIN

        # Groups to hold visual elements
        orbits = VGroup()
        spheres = VGroup()
        trackers = []

        # Create circles and spheres
        for i, r in enumerate(radii):
            # Circle (orbit path)
            orbit = Circle(radius=r, color=GRAY, stroke_opacity=0.3)
            orbit.move_to(center)
            orbits.add(orbit)

            # Dot/sphere
            dot = Dot(radius=0.1, color=BLUE_E).set_z_index(1)

            # Initial angle offset for even spacing
            angle0 = 2 * PI * i / num_spheres
            tracker = ValueTracker(angle0)

            # Angular speed (omega = v / r)
            omega = linear_speed / r

            # Define movement updater
            def update_dot(mob, t=tracker, radius=r):
                angle = t.get_value()
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                mob.move_to(center + [x, y, 0])

            dot.add_updater(update_dot)
            spheres.add(dot)
            trackers.append((tracker, -omega))  # Negative for clockwise

        self.add(orbits, spheres)

        # Animate: increment each tracker
        self.play(*[
            tracker.animate.increment_value(omega * duration)
            for tracker, omega in trackers
        ], run_time=duration, rate_func=linear)

        self.wait()
