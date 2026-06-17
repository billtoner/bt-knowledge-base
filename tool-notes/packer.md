# packer

Build identical machine/container images from a single source config.

## Build

```bash
packer init .                          # install required plugins
packer fmt -recursive .                # format .pkr.hcl
packer validate .                      # check templates
packer build .                         # build all sources
packer build -only=amazon-ebs.web .    # build a single source
```

## Variables & debug

```bash
packer build -var 'region=us-west-2' .
packer build -var-file=prod.pkrvars.hcl .
PACKER_LOG=1 packer build .            # verbose logging
packer build -debug .                  # step through; keep the instance on failure
```

## Notes

- HCL2 templates: `source` blocks (builders) + a `build` block (provisioners)
- Pairs with shell/Ansible provisioners to bake configuration into the image
