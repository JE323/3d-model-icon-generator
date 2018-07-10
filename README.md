# Blender Icon & Thumbnail Generator

This package uses Blender3D from the command line to generated images of models to be used as icons or thumbnails, the idea being this would be incorperated as part of an automated pipeline. See the roadmap to check on what features will be coming soon.

This package is WIP and as such is not currently functional. Please check back soon.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Download the github package.

### Prerequisites

Blender 3D 2.79 - tested on 2.79a

### Installing

Follow the instructions provided by Blender3D for how to install the software. https://docs.blender.org/manual/en/dev/getting_started/index.html

## Running the tests

No tests are currently implememnted, but an explaination will be here once available.

## Deployment

No addition considerations are needed for deployment on a live system. There may be additional software to be written as an interface, however please contribute if it is of benefit to the community.

## Contributing

If you would like to contribute please get in touch first with the functionality you would like to add with a short description of the new feature or bug/issue you would like to fix.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/JE323/blender-icon-generator/tags). 

## Roadmap

* Base render functionality to be implemented in python with an example process being called from a batch file, including importing an object file and rendering out an image.
* Implementation of the camera position to be automatically set - this is considered the final core item for V0.1
* Implementation of basic post-processing and additional render settings
* Implementation of configuration file being set from .json
* Written documentation of the system
* Automated testing of the system 
* Development of a C# service that is setup with a FileSystemWatcher to auto generate new images automatically
* Implementation of whitelist and blacklist filtering for the C# service

## Authors

* **J E** - *Initial work / Developer* - [J E](https://github.com/JE323)

See also the list of [contributors](https://github.com/JE323/blender-icon-generator/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This wouldn't be possible without Blender3D, so thanks for the awesome work that team does!
