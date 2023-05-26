# singularity

Singularity is an open ended project that I'll use to learn about and produce ML models and their dependent runtimes.  The overall thesis is that while massive billion wide feature models generalize well across tasks, similar results can be created with architectures built with many smaller more focused models working together. 

## structure

The singularity project will be divided into "types" which represent different stages of development.  The first will be "Type-A" which will be written primarily in python and represent a prototyping step.  Type-B will take the core findings from Type-A and re-implement both the training and runtime in Rust.  Here, the goal will be to run in as small a footprint as possible; likely embedded systems.
