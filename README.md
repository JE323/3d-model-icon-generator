<h1 align="center">3D Model Icon Generator</h1>

# Overview

3D Model Icon Generator generates icons when provided with a 3D model.

This uses Blender3D from the command line to generated images of models to be used as icons or thumbnails, the idea being this would be incorperated as part of an automated pipeline. Currently, .obj and .fbx model files are supported.

## Table of Contents

- [Overview](#overview)
- [Table of Contents](#table-of-contents)
- [1 - Installation](#1---installation)
  - [1.1 - Compatibility](#11---compatibility)
- [2 - Getting Started](#2---getting-started)
  - [2.1 - Install Blender 3D](#21---install-blender-3d)
- [3 - Usage](#3---usage)
  - [3.1 - Customisation](#31---customisation)
  - [3.2 - Workflow Integration](#32---workflow-integration)
- [4 - About](#4---about)
  - [4.1 - Versioning](#41---versioning)
  - [4.2 - Contributing](#42---contributing)
- [5 - License](#5---license)
- [6 - Acknowledgments](#6---acknowledgments)

## [1 - Installation](#table-of-contents)

### [1.1 - Compatibility](#table-of-contents)

This tool was tested with Blender 3D 2.79a.

For releases, please refer to the [**Release**](https://github.com/JE323/model-thumbnail-generator/releases) page.

## [2 - Getting Started](#table-of-contents)

### [2.1 - Install Blender 3D](#table-of-contents)
 
Follow the instructions provided by Blender3D for how to install the software. https://docs.blender.org/manual/en/dev/getting_started/index.html

Download the github package.

## [3 - Usage](#table-of-contents)

### [3.1 - Customisation](#table-of-contents)

.\triggerRender.ps1 -file "..\..\ExampleObjects\nut.fbx" -output "..\..\Output\"


### [3.2 - Workflow Integration](#table-of-contents)



## [4 - About](#table-of-contents)

### [4.1 - Versioning](#table-of-contents)

This project uses [SemVer](http://semver.org/) for versioning. For releases, please refer to the [**Release**](https://github.com/JE323/model-thumbnail-generator/releases) page.

### [4.2 - Contributing](#table-of-contents)

If you would like to contribute please get in touch first with the functionality you would like to add with a short description of the new feature or bug/issue you would like to fix.

The list of contributors who have contributed can be found [here](https://github.com/JE323/blender-icon-generator/contributors).

## [5 - License](#table-of-contents)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use these files except in compliance with the License. See the [LICENSE.md](LICENSE.md) file for details.

## [5 - Acknowledgments](#table-of-contents)

Thanks to the team at Blender Foundation who produce Blender3D for the great work they do!
