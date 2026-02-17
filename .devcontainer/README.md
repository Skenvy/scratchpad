<!-- containers.dev -->
[devcontainers]: https://containers.dev/
[spec]: https://containers.dev/implementors/spec/
[supported tools]: https://containers.dev/supporting
[cli]: https://containers.dev/implementors/reference/
[devcontainer.json]: https://containers.dev/implementors/json_reference/
[spec devcontainer.json location]: https://containers.dev/implementors/spec/#devcontainerjson
[templates]: https://containers.dev/templates
<!-- codespaces -->
[codespaces]: https://docs.github.com/en/codespaces
[account codespaces]: https://github.com/codespaces
[mcr.microsoft.com/devcontainers/universal]: https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/universal/about
[universal image README]: https://github.com/devcontainers/images/blob/main/src/universal/README.md
[universal image `Dockerfile`]: https://github.com/devcontainers/images/blob/main/src/universal/.devcontainer/Dockerfile
[universal image versions]: https://github.com/devcontainers/images/tree/main/src/universal/history
[mcr search for "container images"]: https://mcr.microsoft.com/en-us/catalog?search=container%20images
[mcr.microsoft.com/devcontainers/base]: https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/base/about
[base-alpine]: https://github.com/devcontainers/images/tree/main/src/base-alpine
[base-debian]: https://github.com/devcontainers/images/tree/main/src/base-debian
[base-ubuntu]: https://github.com/devcontainers/images/tree/main/src/base-ubuntu
[Introduction to dev containers]: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
[Using the default dev container configuration]: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers#using-the-default-dev-container-configuration
[codespace hostRequirements]: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/setting-a-minimum-specification-for-codespace-machines
<!-- vsc -->
[vsc extension]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[Developing inside a Container]: https://code.visualstudio.com/docs/devcontainers/containers
[Create a Dev Container]: https://code.visualstudio.com/docs/devcontainers/create-dev-container
[Dev Container CLI]: https://code.visualstudio.com/docs/devcontainers/devcontainer-cli
[vsc sharing-git-credentials]: https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials
[`.gitattributes` line endings tip]: https://code.visualstudio.com/docs/remote/troubleshooting#_resolving-git-line-ending-issues-in-wsl-resulting-in-many-modified-files
<!-- misc generic -->
[docker]: https://www.docker.com/
[OCI]: https://opencontainers.org/
[moby]: https://mobyproject.org/
[podman]: https://podman.io/
[gitattributes]: https://git-scm.com/docs/gitattributes
[SO: sharing ssh wtih container]: https://stackoverflow.com/questions/75449081
[SO: Normalise line endings]: https://stackoverflow.com/a/15646791/9960809
<!-- misc specific to this repo (or any one of my repos) -->
[my dotfiles]: https://github.com/Skenvy/dotfiles/tree/main/.devcontainer
[my `install.sh`]: https://github.com/Skenvy/dotfiles/blob/main/install.sh
[configure a dev container e.g.]: https://github.com/Skenvy/scratchpad/new/main?dev_container_template=1&filename=.devcontainer%2Fdevcontainer.json
[Skenvy/scratchpad codespaces]: https://github.com/Skenvy/scratchpad/codespaces
[configure and create / new with options...]: https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=900548071
[repo codespaces settings]: https://github.com/Skenvy/scratchpad/settings/codespaces

# [Devcontainers](https://github.com/Skenvy/scratchpad/blob/main/.devcontainer/README.md)
> [!CAUTION]
> These are just some notes on testing the experience of setting up [devcontainers][devcontainers], a convenient wrapper that makes developing in configurable containers _easier_ by providing a tool that does many things OotB that have always been possible but cumbersome.
>
> I've organised these in a way that makes them make the most sense to me but probably aren't easy to read unless I've linked you to a specific section or highlighted note.
> 
> I previously invested time and effort in figuring out how to support [my dotfiles][my dotfiles] (see [my `install.sh`][my `install.sh`]) for use with the devcontainer feature that lets you install dotfiles via a link to a repository, but I never followed it up with any time to figure out how to actually use devcontainers locally or the best way to set them up..

[Devcontainers][devcontainers], although having an open published [spec][spec], and are generally in the process of being adopted by IDES / various-development-platforms, also publishes a list of [supported tools][supported tools], which tracks which tools currently implement the [spec][spec] and to what extent.

There exists a "reference implementation" [cli][cli], but other than that, the tools which most readily, and early, adopted the [spec][spec], are primarily the two Microsoft products: for their tool VS Code, through a [vsc extension "Dev Containers"][vsc extension] and through their platform, GitHub [codespaces][codespaces].

> [!IMPORTANT]
> To work _locally_ with any implementation of the devcontainer [spec][spec], we'll need to make sure we have installed [docker][docker], or some other [OCI][OCI] compliant tool e.g. ([moby][moby] or [podman][podman]). We could theoretically work with a service that hosts the containers, with GitHub codespaces being the prime example of this. But to use devcontainers _locally_, we'll need some OCI tool.

Even though we focus on setting up devcontainers for use with both vsc and gh here, they have fairly different suggested initial configurations, and different experiences of setting up via their native platforms, so we cover what those experiences are to figure out what is the best overall approach.

> [!NOTE]
> GitHub and VS Code are both products of Microsoft, so there is significant overlap of their documentation, and they liberally make use of linking between their docs, much more so from the codespace docs on GitHub making frequent use of linking to explanations / guides in the vsc docs, though. Which is worth mentioning here because although we start off with a look at the codespace docs, we don't preemptively follow those links to the vs code docs until we get to that section. Which means large chunks of the github docs that just act as precursors / wrappers / restatements of the vs code docs are discluded from this summary.

## spec / generic
Before diving in to codespaces and the vsc extension, it's worth highlighting some pieces of the spec, or at least, mentioning them here if they are implied but not specifically spelled out later. As well as some generic tips. In no particular order...

### `devcontainer.json` order of precedence
There is an order in which different `devcontainer.json` files will be looked for to use, according to [this][spec devcontainer.json location]. To "quote" the spec:
* 1st is `<repo-root>/.devcontainer/devcontainer.json`
* 2nd is `<repo-root>/.devcontainer.json`
* 3rd is `<repo-root>/.devcontainer/<folder>/devcontainer.json` (where `<folder>` is a sub-folder, one level deep)

You can use these various potential paths to include multiple different `devcontainer.json` configurations, with an order of precedence.

### Set your `.gitattributes` to avoid false positive changes
See this [`.gitattributes` line endings tip][`.gitattributes` line endings tip]. (Or the git docs on [gitattributes][gitattributes]).

To prevent many false positive changes being committed and frequently rewriting files to swap line endings back and forth, you should ensure you set your `.gitattributes` file to normalise your file line endings in your index. A simple setup is a `.gitattributes` file of:
```
* text=auto eol=lf
*.cmd text eol=crlf
*.bat text eol=crlf
```
If you've just added this, you'll also want to run `git add --renormalize .` (see [this SO answer][SO: Normalise line endings]) and commit the renormalised line endings.

## GitHub Codespaces
[Codespaces][codespaces] are best thought of as a service GitHub provides as a "layer of management" over the use of devcontainers in a repo, but it can be used without setting up or configuring any devcontainers, by way of a "default" devcontainer. While setting up initially, focussing solely on vsc and ignoring gh might offer a greater degree of freedom, but it would be easier to start from what features of devcontainers gh codespaces puts front and center, before branching out to see what other options exist.

It's possible to configure your own devcontainers and use them in codespaces, or to have no config at all and simply use whatever the default config is. If you're using the default (or any other gh provided containers) you can use...
```sh
# in your container's shell
devcontainer-info # output like ~
# - Definition ID: universal
# - Source code repository: https://github.com/devcontainers/images
```
...to get info about the running image.

### "Configure a dev container"
If you don't have any config yet, or you maybe do but still pick this option from the gh UI, the experience of "setting up devcontainer config" via what gh suggests will go as follows:

---
If you select to "`configure a dev container`" from the "`<> Code`" -> "`Codespaces`" -> "`...`" drop down menu you'll be taken to a link that looks like:
* i.e. `https://github.com/<owner>/<repo>/new/<trunk>?dev_container_template=1&filename=.devcontainer%2Fdevcontainer.json`
* e.g. [`https://github.com/Skenvy/scratchpad/new/main?dev_container_template=1&filename=.devcontainer%2Fdevcontainer.json`][configure a dev container e.g.]

Which will want to add a file `<repo-root>/.devcontainer/devcontainer.json` which is simply
```json
{
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "features": {}
}
```
Plus a side panel with a tab explaining how "`Features`" work and a tab offering a range of "`Features`" to choose from.

### Default devcontainer image
The image suggested for use by the above process, [mcr.microsoft.com/devcontainers/universal][mcr.microsoft.com/devcontainers/universal], is codespace's default devcontainer image.

You can read about it in the gh docs on "[Using the default dev container configuration][Using the default dev container configuration]."

Or you can read the [universal image README][universal image README] which describes the `Linux Universal Image`, which offers a build of this [universal image `Dockerfile`][universal image `Dockerfile`].

You can track down which commit of that [`Dockerfile`][universal image `Dockerfile`] built any particular tag of the universal image by reading the [universal image versions][universal image versions].

Note according to [this][Using the default dev container configuration] that "GitHub does not charge for storage of containers built from the default dev container image."

If it's possible/reasonable for you to run a container from a base image that is a tag of the default `universal` image, and simply apply features on top for whatever it doesn't provide already that you still need, then doing so can save your container costs in the codespaces service.

### Codespaces misc
* You can see your repository codespaces by simply adding `/codespaces` to the end of your repo url:
    * i.e. `https://github.com/<owner>/<repo>/codespaces`
    * e.g. [`https://github.com/Skenvy/scratchpad/codespaces`][Skenvy/scratchpad codespaces]
* There's also an account view of codespaces at [`https://github.com/codespaces`][account codespaces]
* the options if you try to [configure and create / new with options...][configure and create / new with options...] are limited to branch, region, and machine type, and don't expose any of the devcontainer options at that stage.
* The current [repo codespaces settings][repo codespaces settings] are limited to configuring prebuilds.
* Although `universal` is the default image, there is also a `base` image, [mcr.microsoft.com/devcontainers/base][mcr.microsoft.com/devcontainers/base].
    * [`base-alpine`][base-alpine]
    * [`base-debian`][base-debian]
    * [`base-ubuntu`][base-ubuntu]
* The `"hostRequirements"` option in the [devcontainer.json][devcontainer.json] can be configured for codespaces like [this][codespace hostRequirements].

## VS Code Extension
The [vsc extension][vsc extension] is required for this section. It does a lot of the heavy lifting of suggesting different templates.
### Recommend the extension to anyone opening your repo in vsc
If you are adding devcontainers to a repo that you are setting up specifically for use in vsc, you can also "recommend" the extension to anyone via a JSONC file `<repo-root>/.vscode/extensions.json`:
```jsonc
{
  "recommendations": [
    "ms-vscode-remote.remote-containers",
  ]
}
```
### Getting started
You can read the vsc overview "[Developing inside a Container][Developing inside a Container]".

For this, we want to know how to see what possible configurations are either suggested or what we can add. Opening the command palette, `Dev Containers: Open Folder in Container...` would let us choose an existing already present config to use, but we can use `Dev Containers: Add Dev Container Configuration Files...` instead. If we do this we get a drop down list to choose from. If we pick `Show all templates...` and then `Learn more`, we get taken to the devcontainer site's own list of [templates][templates], which mentions:
> Templates listed here will be presented in the UX of [supporting tools][supported tools].

As an example, you search for "universal" to see if it offers a template for the same default image as GitHub does, you'll see that there is an option called "Default Linux Universal" which creates the following `<repo-root>/.devcontainer/devcontainer.json` (ignoring the option to add features or configure dependabot):
```jsonc
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
// README at: https://github.com/devcontainers/templates/tree/main/src/universal
{
	"name": "Default Linux Universal",
	// Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
	"image": "mcr.microsoft.com/devcontainers/universal:5-linux"

	// Features to add to the dev container. More info: https://containers.dev/features.
	// "features": {},

	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	// "forwardPorts": [],

	// Use 'postCreateCommand' to run commands after the container is created.
	// "postCreateCommand": "uname -a",

	// Configure tool-specific properties.
	// "customizations": {},

	// Uncomment to connect as root instead. More info: https://aka.ms/dev-containers-non-root.
	// "remoteUser": "root"
}
```
If we try to use the option to `Dev Containers: Add Dev Container Configuration Files...` a second time, it will warn us that one already exists. If we continue we can set up a new one, and simply get the option to either overwrite the existing `<repo-root>/.devcontainer/devcontainer.json`, or skip. I can't seem to locate any way to get the template selector to suggest or imply that we have the option of adding a `devcontainer.json` inside a one folder deep nest inside the `<repo-root>/.devcontainer` folder, if we want to try and create more.
### vsc misc
* You can share your SSH and GPG keys with a local container. See [sharing-git-credentials][vsc sharing-git-credentials].
## We've tried both default bare setups, what next?
We have tried both the GitHub and VS Code paths to setting up the default bare universal config, what now?

So far we've been exposed to two methods of getting roughly the same result: a single `<repo-root>/.devcontainer/devcontainer.json` file that looks something like
```jsonc
{
  "name": "<Some name>",
  "image": "<some image>",
  // Some comments, because this is JSONC.
  // And some features object we are yet to use.
  "features": {}
}
```
The template we created in vsc had several more comments to suggest features to use, but at this point, we might need to keep a tab open on the reference page for [devcontainer.json][devcontainer.json] config.
### Dockerfile / Docker-Compose
We can see in the [devcontainer.json][devcontainer.json] that we can specify to build a `Dockerfile` or use a `compose.yaml` with multiple targets.
