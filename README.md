# singularity

Singularity is an open ended project that I'll use to learn about and produce ML models and their dependent runtimes.  The overall thesis is that while massive billion wide feature models generalize well across tasks, similar results can be created with architectures built with many smaller more focused models working together. 

## Stages

The singularity project will be divided into "types" which represent different stages of development.
### Type-A: human crafted
The first will be "Type-A" which will be written primarily in python and represent a prototyping step. The goal here is to quickly develop and prototype ideas around multiple small models workting together.  It will use third party libraries and integrate with services like huggingface.

### Type-B: Hybrid standalone 
Type-B will take the core findings from Type-A and re-implement both the training and runtime in Rust.  The code here will be completely standalone, not requiring any third party libraries.  Code here will be a mix of human and AI generated and will explore what the project structure necessary for AI generated code to be commited and evaluated.

### Type-C: Generated Autonomously
Type-C will be untouched by human hands and be completely created and maintained autonomously.  Likely it will take the overall structure of the Type-B codebase but be structured in a way that can be understood, updated, and maintained by an autonomous agent.

## Docker

Docker Containers are used extensively in the project.  Using docker containers allows a separation of concerns between the running code and the environment that it is running on.  Distinct containers allow clean-room like control over the operating system, third party dependencies, and even access to the hardware made accessible at runtime.  

Details about each of the docker containers used in the project can be found in the [`docker/`](docker/README.md) 




