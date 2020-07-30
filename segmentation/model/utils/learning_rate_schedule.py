import tensorflow as tf

"""
Custom learning rate scheduler for yolact 
"""


class Yolact_LearningRateSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):

    def __init__(self, warmup_steps, warmup_lr, initial_lr):
        """
        :param warmup_steps:
        :param warmup_lr:
        :param initial_lr:
        """
        super(Yolact_LearningRateSchedule, self).__init__()
        self.warmup_step = warmup_steps
        self.warmup_lr = warmup_lr
        self.initial_lr = initial_lr

    def __call__(self, step):
        learning_rate = tf.convert_to_tensor(self.warmup_lr)
        dtype = learning_rate.dtype
        warmup_steps = tf.cast(self.warmup_step, dtype)
        lr = tf.cast(self.initial_lr, dtype)

        def f0():return (lr - self.warmup_lr) * (step / self.warmup_step) + self.warmup_lr
        def f1():return 1e-5
        def f2():return 1e-6
        def f3():return 1e-7
        def f4():return 1e-8
        def f5():return 1e-9

        learning_rate = tf.case([(tf.math.logical_and(tf.math.less(warmup_steps, step), tf.less_equal(step, 3000.)), f1),
                                 (tf.math.logical_and(tf.math.less(3000., step), tf.less_equal(step, 10000.)), f2),
                                 (tf.math.logical_and(tf.math.less(10000., step), tf.less_equal(step, 20000.)), f3),
                                 (tf.math.logical_and(tf.math.less(20000., step), tf.less_equal(step, 50000.)), f4),
                                 (tf.math.greater(step, 50000.), f5)],
                                default=f0,
                                exclusive=True)

        return learning_rate

    def get_config(self):
        return {
            "warm up learning rate": self.warmup_lr,
            "warm up steps": self.warmup_steps,
            "initial learning rate": self.initial_lr
        }


if __name__ == '__main__':
    lr = Yolact_LearningRateSchedule(warmup_steps=500, warmup_lr=1e-4, initial_lr=1e-4)
    lr(100.)
    print()