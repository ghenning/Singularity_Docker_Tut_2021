# Docker/Singularity Tutorial

[**Singularity installation guide**](https://sylabs.io/guides/3.4/user-guide/installation.html)

[**Docker installation guide**](https://docs.docker.com/install/)

[**How to run Docker without 'sudo'**](https://docs.docker.com/install/linux/linux-postinstall/)

## Quick notes on Docker and Singularity

Docker/Singularity are virtualization through containers.
Each container has their own software/environments/...
Makes it easy to version control software. You can run
the same version of a software on any machine that has
Docker/Singularity. 
You create containers that you use from images.
By now, images of pretty much anything exist, so you rarely
need to build your own image, just pull the one you need (e.g. dockerhub).
**NOTE** *The Documentation for Docker and Singularity is very extensive
and helpful. This should be your first place to look while troubleshooting.*

## Where is it on our machines?

Docker can be found on the paf and pacifix machines. The access to
those machines is limited to a few people, so you'll most likely only
have access to machines with Singularity. 
**Why?** *Docker can be dangerous on remote machines (or even your
local machine) if you're not careful. You usually get root privileges,
so you'd be capable of accidentally (or not) deleting important stuff.
That's why Singularity is the go-to container service on our machines.*

Singularity is on dogmatix and hercules (and probably more).
Singularity images are literal image files from where you make
your containers. You need to create your image and copy it to the
machine where you want to use it (if you can't build it on that machine).

## Hello World
Check if your installation works
```
docker pull hello-world
docker run hello-world
```

## Docker pull

Pull an existing image from dockerhub
```
docker pull <image name:tag>
```
*(tag is optional, otherwise pulls latest version)*

Most of the software we use can be found at the [MPIfR dockerhub page](https://hub.docker.com/u/mpifrpsr)

To see the images you have, run
```
docker images
```
and if you want to get rid of an image, run
```
docker rmi <image>
```

## Dockerfile

You can build your own image from a Dockerfile.
The Dockerfile contains all the terminal commands you
would use to install software. To build an image from
a Dockerfile, cd into the directory where you Dockerfile is
and run
```
docker build -t <name:tag> .
```
*(tag is optional)*

## Launching container

### Basic usage

You can start a container by opening an interactive shell
within it, or simply let it do its thing in the background.

To open a terminal in container
```
docker run --rm -ti <image name> bash
```
The `rm` tag will delete the container once you exit it and is
completely optional, but helps with keeping things neat and tidy.
'ti' enables interactive shell. 
To detach from a container (leaving the shell without closing the
container) you press `[ctrl]+[p]+[q]`. To exit a container you do
it the same way you would with a normal terminal, `[ctrl]+[d]` or
write `exit`.
To see runing containers...

### Mounting volumes

You can mount directories with the **-v** tag, e.g.
```
docker run --rm -ti -v /home/batman/work/non_detections/:<path within container> ...
```
The **path within container** can be whatever you like. However, it is often
convenient to use the directory structure as it is in the file system. 
That way your code will not freak out if it depends on the file system's 
directory structure. This can also help you realizing where you are working.
Long path strings can be annoying though, so it's also a good idea to just
use simple, concise catchwords, e.g. **/work**, **/data**,...

Example
```
docker run --rm -ti -v /home/batman/work/non_detections/:/home/batman/work/non_detections ...
docker run --rm -ti -v /home/batman/work/non_detections/:/data ...
```
*NOTE: You can mount as many directories as you need*

### User privileges

In Docker you are root by default *(dangerous)*. This can also cause problems
accessing files created within the Docker image. The **-u** tag solves this, as it
forwards your user and group IDs.

```
docker run --rm -ti -u <UID>:<GID> ...
```

### Putting it all together

Using the example code in this repository.

First clone this repo to your computer
```
git clone git@github.com:ghenning/PulsarTutorialJan2020.git
```
and cd into the **docker** directory. We will build a simple Docker image
from the Dockerfile there, which includes Python and some packages.
``` 
docker build -t simple_py .
```
*(you can name the image whatever you like)*

In the **code** directory is a tiny python script which reads in a two column data file
and saves a plot of the data. This is a very familiar setup, where we have our **code**,
**data**, and **results**. Start by making a directory called **results**. 

Now we use all of the above information run a Docker container which runs a script which reads
in data from somewhere else, and spits out results in another directory.
```
docker run --rm -u 1000:1000 -v /home/batman/work/PulsarTutorialJan2020/code/:/code
    -v /home/batman/work/PulsarTutorialJan2020/data/:/data
    -v /home/batman/work/PulsarTutorialJan2020/results/:/results
    simple_py python /code/example_program.py --data /data/data.txt --outdir /results
```
This should create a figure in your results directory.

## Moving to Singularity

Singularity is available on many of our computers, so we need to convert our Docker
image to Singularity. 
One such way is to use [**docker2singularity**](https://github.com/singularityhub/docker2singularity)
```
docker run -v /var/run/docker.sock:/var/run/docker.sock 
    -v <your output dir>:/output 
    --privileged -t --rm 
    singularityware/docker2singularity 
    <image to convert>
```
where **your output dir** is where you want to store your Singularity image,
and **image to convert** is the Docker image which you want to convert.

*NOTE: Singularity images are stored as files on your computer, so you can NOT
run something like 'singularity images' to list your images. Store your Singularity
images in one place so you won't lose them. You only need to build your Singularity
image once, and then transfer it to the machine where you need to use it.*

### Using Singularity

The usage of singularity is more or less identical to Docker, with only some differences
in syntax. 

To run a terminal on a container (like *docker run ... bash*) 
```
singularity shell <path to image>
```
where **path to image** is where you store your image (just type in the image name if you're
within the same directory as the image).

Singularity keeps your privileges, so a tag like **-u** from Docker is not required.

To mount directories use **-B**.

To run something from within Singularity without using a terminal, use **exec**.

If we run the same reading/plotting data code from before using Singularity, it will
look like this
```
singularity exec -B /home/batman/work/PulsarTutorialJan2020/code/:/code
    -B /home/batman/work/PulsarTutorialJan2020/data/:/data
    -B /home/batman/work/PulsarTutorialJan2020/results/:/results
    /home/batman/work/singularity_images/simple_py.simg
    python /code/example_program.py --data /data/data.txt --outdir /results
```
