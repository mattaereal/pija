PIJA: Pornographic images jacking algorithm
===========================================

Pija is a proof of concept about how malware can easily detect and steal homemade adult content from the victim's computer.

This PoC only contains the detection bits of the concept, but can be further improved using different techniques such as biometrics and metadata analysis to find matches between suspicious pictures and victim's social network's photos.

Ths was developed as part of a presentation we (@alcuadrado & @mattaereal) gave at [Ekoparty](www.ekoparty.org) 2013. You can watch it [here](http://vimeo.com/77523121) (spanish) and grab the slides from [here](http://www.ekoparty.org//archive/2013/charlas/slides.tar.gz) (mostly spanish).

## Dependencies

* python 2.7
* python-opencv 2
* scipy 0.12
* numpy 1.7
* termcolor 1.1.0
* python-magic 0.4.3

## Running it

Just run:

`pija <FILES>`

or:

`pija -R <FOLDER>`

## References

* "An algorithm for nudity detection", Rigan Ap-apid.
* "Image-based pornography detection", Rigan Ap-apid.
* "Explicit image detection using YCbCr space color model as skin detection", Marcial Basilio, Aguilar Torres , et al.
* "Optimization of automatic nudity detection in high-resolution images with the use of NuDetective Forensic Tool", da Silva Eleuterio, Castro Polastro.
* "Nudity detection based on image zoning", Clayton Santos, Eulanda M. dos Santos, Eduardo Souto
* "Machine learning application on detecting nudity in images", Yong Lin, Yujun Wu.
