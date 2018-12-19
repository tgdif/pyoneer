import tensorflow as tf


def policy_ratio_loss(log_probs,
                      log_probs_anchor,
                      advantages,
                      epsilon_clipping=0.2,
                      weights=1.0):
    log_probs_anchor = tf.stop_gradient(log_probs_anchor)

    ratio = tf.exp(log_probs - log_probs_anchor)
    ratio = tf.check_numerics(ratio, 'ratio')

    surrogate1 = ratio * advantages
    surrogate1 = tf.check_numerics(surrogate1, 'surrogate1')

    surrogate2 = tf.clip_by_value(ratio, 1 - epsilon_clipping,
                                  1 + epsilon_clipping) * advantages
    surrogate2 = tf.check_numerics(surrogate2, 'surrogate2')

    surrogate_min = tf.minimum(surrogate1, surrogate2)
    surrogate_min = tf.check_numerics(surrogate_min, 'surrogate_min')

    loss = -tf.losses.compute_weighted_loss(
        losses=surrogate_min, weights=weights)
    loss = tf.check_numerics(loss, 'loss')
    return loss