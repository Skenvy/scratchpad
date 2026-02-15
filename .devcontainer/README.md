# Devcontainers
This is just some notes on testing the experience of setting up [devcontainers](https://containers.dev/), a convenient wrapper that makes developing in configurable containers _easier_ by providing a tool that does many things OotB that have always been possible but cumbersome.

I previously invested time and effort in figuring out how to support my [dotfiles](https://github.com/Skenvy/dotfiles/tree/main/.devcontainer) (see my [install.sh](https://github.com/Skenvy/dotfiles/blob/main/install.sh)) for use with the devcontainer feature that lets you install dotfiles via a link to a repository, but I never followed it up with any time to figure out how to actually use devcontainers locally or the best way to set them up..

Devcontainers are primarily supported at the moment through a [vsc extension "Dev Containers"](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) and through [GitHub codespaces](https://docs.github.com/en/codespaces).
## useful links
* [spec](https://containers.dev/)
* `vsc`
    1. [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)
    1. [Create a Dev Container](https://code.visualstudio.com/docs/devcontainers/create-dev-container)
    1. [devcontainer.json](https://containers.dev/implementors/json_reference/)
    1. [Dev Container CLI](https://code.visualstudio.com/docs/devcontainers/devcontainer-cli)
* `gh`
    1. [Introduction to dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers)

## GitHub Codespaces
Even though we focus on using devcontainers for both vsc and gh here, they have fairly different suggested initial configurations.

This is probably because codespaces are better thought of as a service GitHub provides as a layer of management over the use of devcontainers in a repo, but it can be used without setting up or configuring any devcontainers, by way of its own internal default devcontainer. So while setting up initially for use focussing solely on vsc and ignoring gh might offer a greater degree of freedom, it would be easier to start from what features of devcontainers gh codespaces puts front and center, before branching out to see what other options exist.

---
Info on the default devcontainer gh uses for codespaces if you don't have any configured can be seen [here](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers#using-the-default-dev-container-configuration).

---
Or you can read [this](https://github.com/devcontainers/images/tree/main/src/universal) which describes the `Linux Universal Image` of the [devcontainers/images](https://github.com/devcontainers/images) repo, which offers a build of this [Dockerfile](https://github.com/devcontainers/images/blob/main/src/universal/.devcontainer/Dockerfile).

---
Also note according to [this](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers#using-the-default-dev-container-configuration) that "GitHub does not charge for storage of containers built from the default dev container image."

---
If you select to "`configure a dev container`" from the "`<> Code`" -> "`Codespaces`" -> "`...`" drop down menu you'll be taken to a link that looks like:
* i.e. `https://github.com/<owner>/<repo>/new/<trunk>?dev_container_template=1&filename=.devcontainer%2Fdevcontainer.json`
* e.g. [`https://github.com/Skenvy/scratchpad/new/main?dev_container_template=1&filename=.devcontainer%2Fdevcontainer.json`](https://github.com/Skenvy/scratchpad/new/main?dev_container_template=1&filename=.devcontainer%2Fdevcontainer.json)

Which will want to add a file `<repo-root>/.devcontainer/devcontainer.json` which is simply
```json
{
  "image": "mcr.microsoft.com/devcontainers/universal:2",
  "features": {}
}
```
Plus a side panel with a tab explaining how "`Features`" work and a tab offering a range of "`Features`" to choose from.

---
To address a few details about codespaces..
* "Docs" and "What are codespaces" both link to [GitHub codespaces](https://docs.github.com/en/codespaces).
* You can see your repository codespaces by simply adding `/codespaces` to the end of your repo url:
    * i.e. `https://github.com/<owner>/<repo>/codespaces`
    * e.g. [`https://github.com/Skenvy/scratchpad/codespaces`](https://github.com/Skenvy/scratchpad/codespaces)
* the options if you try to [configure and create / new with options...](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=900548071) are limited to branch, region, and machine type, and don't expose any of the devcontainer options at that stage.
* The current [codespaces settings](https://github.com/Skenvy/scratchpad/settings/codespaces) are limited to configuring prebuilds.


