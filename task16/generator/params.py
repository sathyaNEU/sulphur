"""Every constant of the task16 world. The generator reads nothing else for a number."""

WORLD_SEED = 15
WORLD_TAG = "v3"

# the population and the label process
D_IN = 32
K = 10
TEACHER_J = 1500
TEACHER_GAMMA = 0.6
TEACHER_BETA = 8.0

# labelling routes: the share of labels a route records wrongly (the expert route records the ground truth process)
ROUTE_ERROR = {"A": 0.0, "B": 0.03, "C": 0.16}
POOL = {"A": 128000, "B": 128000, "C": 1024000}
SHARD = 4000
DEV_MIX = {"A": 6000, "B": 1000, "C": 1000}
BENCH_N = 20000

# the group's training recipe
BATCH = 128
EPOCHS = 12
WARMUP = 0.03
DEPTH = 2
ADAM = (0.9, 0.999, 1e-8)

# author-side only: expert-quality labels the lab does not have, to measure what more of them would have given
PRIVATE_EXPERT_POOL = 1024000
