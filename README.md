# singularity

Singularity is an open ended project that I'll use to learn about and produce ML models and their dependent runtimes.  The overall thesis is that while massive billion wide feature models generalize well across tasks, similar results can be created with architectures built with many smaller more focused models working together. 

## structure

The singularity project will be divided into "types" which represent different stages of development.  The first will be "Type-A" which will be written primarily in python and represent a prototyping step.  Type-B will take the core findings from Type-A and re-implement both the training and runtime in Rust.  Here, the goal will be to run in as small a footprint as possible; likely embedded systems.

## Text Processing

This project is based on processing text.  The goal is to be able to process any kind of text and to accomplish that we break text ingress into 3 parts.  Raw Storage, Normalization and Tokenization.

### Raw Storage

Raw storage tries to capture the originating text in as close to it's found state as possible along with metadata of how to re-retrieve that data and any steps taken which modify that original data. 

### Normalization

Normalization step involves converting the raw data into a known structure that can be easily tokenized and processed.  This involves removing the text body from whatever envelope format it exists in its raw state, converting that text body to a suitable encoding, typically UTF-8, and where appropriate adding special tokens that denote semantic structure (start/end of paragraphs, titles, etc.)  The body of the text is stored along with metadata of where/how/when it was extracted.

### Tokenization

Plain text is not a particularly efficient way of storing data for training.  The tokenization step takes the normalized data and converts it into a stream of integer values.  The tokenization is based on a dictionary which is built using a form of BPE.  The building of the dictionary happens after all of the desired documents that will form a training corpus are normalized and is a necessary step before tokenization.  