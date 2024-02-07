# singularity

Singularity is an open ended project that I'll use to learn about and produce ML models and their dependent runtimes.  The overall thesis is that while massive billion wide feature models generalize well across tasks, similar results can be created with architectures built with many smaller more focused models working together. 

## structure

The singularity project will be divided into "types" which represent different stages of development.
### Type-A: human crafted
The first will be "Type-A" which will be written primarily in python and represent a prototyping step. The goal here is to quickly develop and prototype ideas around multiple small models workting together.  It will use third party libraries and integrate with services like huggingface.

### Type-B: Hybrid standalone 
Type-B will take the core findings from Type-A and re-implement both the training and runtime in Rust.  The code here will be completely standalone, not requiring any third party libraries.  Code here will be a mix of human and AI generated and will explore what the project structure necessary for AI generated code to be commited and evaluated.

### Type-C: Generated Autonomously
Type-C will be untouched by human hands and be completely created and maintained autonomously.  Likely it will take the overall structure of the Type-B codebase but be structured in a way that can be understood, updated, and maintained by an autonomous agent.

## Text Processing

This project is based on processing text.  The goal is to be able to process any kind of text and to accomplish that we break text ingress into 3 parts.  Raw Storage, Normalization and Tokenization.

### Raw Storage

Raw storage tries to capture the originating text in as close to it's found state as possible along with metadata of how to re-retrieve that data and any steps taken which modify that original data. 

### Normalization

Normalization step involves converting the raw data into a known structure that can be easily tokenized and processed.  This involves removing the text body from whatever envelope format it exists in its raw state, converting that text body to a suitable encoding, typically UTF-8, and where appropriate adding special tokens that denote semantic structure (start/end of paragraphs, titles, etc.)  The body of the text is stored along with metadata of where/how/when it was extracted.

### Tokenization

Plain text is not a particularly efficient way of storing data for training.  The tokenization step takes the normalized data and converts it into a stream of integer values.  The tokenization is based on a dictionary which is built using a form of BPE.  The building of the dictionary happens after all of the desired documents that will form a training corpus are normalized and is a necessary step before tokenization.  
