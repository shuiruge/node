import tensorflow as tf
from node.wrapper import node_wrapper
from node.fix_grid import FixGridODESolver, rk4_step_fn


data_size = 10
x = tf.constant([[2., 0]])
# x = tf.constant([[-0.1, 2.0], [-2.0, -0.1]])

solver = FixGridODESolver(rk4_step_fn, data_size)
dense = tf.keras.layers.Dense(2)


@node_wrapper(solver, 0.)
@tf.function
def f(x, t):
    x0, x1 = tf.unstack(x, axis=-1)
    y0 = x0 + 2 * x1
    y1 = -3 * x0 + x1
    return dense(tf.stack([y0, y1], axis=-1))


with tf.GradientTape() as g:
    g.watch(x)
    y = f(x, 1.)
print(g.gradient(y, x))
