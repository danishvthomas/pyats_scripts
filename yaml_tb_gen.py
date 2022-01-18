import yaml

"""
devices:
  jumphost:
    os: linux
    type: linux
    connections:
      cli:
        protocol: ssh
        #ip: 172.16.87.128
        ip: 192.168.0.64
    credentials:
        default:                         # login credentials
            username: admin
            password: nbv12345
  CEL7:
    os: iosxe
    type: router
    alias: CEL7
    connections:
      defaults:
        class: unicon.Unicon
      cli:
        command: open /f3225e7f/n0/0
        proxy: jumphost
    credentials:
      enable:
        password: cisco
      default:
        password: cisco
        username: cisco

A: a
B:
  C: c
  D: d
  E: e


"""

data = dict(
    A = 'a',
    B = dict(
        C = 'c',
        D = 'd',
        E = 'e',
    )
)

#with open('data.yml', 'w') as outfile:#
#    yaml.dump(data, outfile, default_flow_style=False)


tb_1 = dict(
  jumphost = dict(
    os = linux,
    type = linux,
    connections = dict(
      cli = dict(
        protocol = ssh,
        ip = '192.168.0.64',
      )
     )
    credentials = dict(
        default = dict(                         # login credentials
            usernam = admin,
            password = nbv12345,
           )
        )
   )
)

with open('tb_1.yml', 'w') as outfile:
    yaml.dump(tb_1, outfile, default_flow_style=False)
