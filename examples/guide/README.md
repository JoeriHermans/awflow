This guide shows the basic usage of `awflow` and illustrates
the motivation behind the project.

Large projects often require you to write a large set of
submission scripts with various parameters and dependencies.
To organize a project such that it is maintainable, individual
submission scripts are usually seperated in different files
with the resource requirements (in the case of Slurm) specified
at the top via `#SBATCH`. This can make tuning the parameters
of the job quite cumbersome, as you'll have to search for the
correct file. Furthermore, many of these individual scripts
often have a lot of redundant code, i.e., setting environment
variables, loading Anaconda or virtualenv, etc.

Other problems occur whenever *a part* of the submission pipeline
has already been computed, but for some reason you have to
rerun a specific part. In such cases, one could simply
comment out part of the submission script. However, the
way dependencies are typically specified in such scripts make it
really cumbersome to do that.

Instead, as we will demonstrate, this module will manage all
of these issues for you. It will do so in such a way you can
develop and test your pipelines / workflows on your
personal machine, but execute it on a HPC system whenever
you are satisfied with your pipeline's functionality.
