from dinner_helper import Philosopher


class DiningPhilosopher(Philosopher):

    def dining(self):
        thinked = False
        while not self.dinner_end.is_set():
            if not thinked:
                self.think()
                thinked = True
            right_taken = self.right_fork.take()
            if not right_taken:
                continue
            left_taken = self.left_fork.take(timeout=self.eat_time)
            if left_taken and right_taken:
                self.eat()
                thinked = False
            if right_taken:
                self.right_fork.release()
            if left_taken:
                self.left_fork.release()
