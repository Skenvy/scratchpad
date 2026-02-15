<!-- containers.dev -->
[devcontainers]: https://containers.dev/
[spec]: https://containers.dev/implementors/spec/
[supported tools]: https://containers.dev/supporting
[cli]: https://containers.dev/implementors/reference/
[devcontainer.json]: https://containers.dev/implementors/json_reference/
[spec devcontainer.json location]: https://containers.dev/implementors/spec/#devcontainerjson
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
<!-- vsc -->
[vsc extension]: https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
[Developing inside a Container]: https://code.visualstudio.com/docs/devcontainers/containers
[Create a Dev Container]: https://code.visualstudio.com/docs/devcontainers/create-dev-container
[Dev Container CLI]: https://code.visualstudio.com/docs/devcontainers/devcontainer-cli
<!-- misc -->
[my dotfiles]: https://github.com/Skenvy/dotfiles/tree/main/.devcontainer
[my `install.sh`]: https://github.com/Skenvy/dotfiles/blob/main/install.sh
[configure a dev container e.g.]: https://github.com/Skenvy/scratchpad/new/main?dev_container_template=1&filename=.devcontainer%2Fdevcontainer.json
[Skenvy/scratchpad codespaces]: https://github.com/Skenvy/scratchpad/codespaces
[configure and create / new with options...]: https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=900548071
[repo codespaces settings]: https://github.com/Skenvy/scratchpad/settings/codespaces

# [Devcontainers](https://github.com/Skenvy/scratchpad/blob/main/.devcontainer/README.md)
> [!WARNING]
> These are just some notes on testing the experience of setting up [devcontainers][devcontainers], a convenient wrapper that makes developing in configurable containers _easier_ by providing a tool that does many things OotB that have always been possible but cumbersome.
>
> I've organised these in a way that makes them make the most sense to me but probably aren't easy to read unless I've linked you to a specific section or highlighted note.
> 
> I previously invested time and effort in figuring out how to support [my dotfiles][my dotfiles] (see [my `install.sh`][my `install.sh`]) for use with the devcontainer feature that lets you install dotfiles via a link to a repository, but I never followed it up with any time to figure out how to actually use devcontainers locally or the best way to set them up..

[Devcontainers][devcontainers], although having an open published [spec][spec], and are generally in the process of being adopted by IDES / various-development-platforms, also publishes a list of [supported tools][supported tools], which tracks which tools currently implement the [spec][spec] and to what extent.

There exists a "reference implementation" [cli][cli], but other than that, the tools which most readily, and early, adopted the [spec][spec], are primarily the two Microsoft products: for their tool VS Code, through a [vsc extension "Dev Containers"][vsc extension] and through their platform, GitHub [codespaces][codespaces].

Even though we focus on setting up devcontainers for use with both vsc and gh here, they have fairly different suggested initial configurations, and different experiences of setting up via their native platforms, so we cover what those experiences are to figure out what is the best overall approach.

## spec
Before diving in to codespaces and the vsc extension, it's worth highlighting some pieces of the spec, or at least, mentioning them here if they are implied but not specifically spelled out later. In no particular order...

### `devcontainer.json` order of precedence
There is an order in which different `devcontainer.json` files will be looked for to use, according to [this][spec devcontainer.json location]. To "quote" the spec:
* 1st is `<repo-root>/.devcontainer/devcontainer.json`
* 2nd is `<repo-root>/.devcontainer.json`
* 3rd is `<repo-root>/.devcontainer/<folder>/devcontainer.json` (where `<folder>` is a sub-folder, one level deep)

You can use these various potential paths to include multiple different `devcontainer.json` configurations, with an order of precedence.

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

## VS Code Extension
The [vsc extension][vsc extension].
