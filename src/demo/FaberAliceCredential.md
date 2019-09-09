# Faber Alice Demo

The goal of this document is to flesh out the open API demo described here:

https://github.com/hyperledger/aries-cloudagent-python/blob/master/demo/AriesOpenAPIDemo.md

but using the command line aca-py 0.3.1 and include the steps needed to create the public DIDs, schema and credential definition not included above.  Also wanted to use a different credential just to better understand the process

## Setup

Notes each the ledger is restarted must must wipe
out wallets so that they are in sync.  The wallet stores credential definitions, connections, DIDs and credentials.  Otherwise we must persist the ledger state across invocations of ledger.


## 1) Run the local indy ledger using docker.


```bash
$ cd /.../indy/indy-sdk/
$ docker run -itd -p 9701-9708:9701-9708 indy_pool
$ docker container ls
 ...  xenodochial_hermann
```

Later to stop ledger pool do

```bash
$ docker container stop xenodochial_hermann
```


## 2) Run the von-network web server ledger browser


```bash

$ cd /.../von-network/
$ GENESIS_FILE=/Data/Code/public/hyperledger/aries/cloudagentpy/demo/local-genesis.txt PORT=9000 REGISTER_NEW_DIDS=true python3 -m server.server

```

Later to stop use

```bash
^-C ^-C
```

If later rebuild indy pool then pull latest von-network

Navigate web browser to:
```
http://localhost:9000
```

## 3) Use von-network browser to create public DID for Faber.

Navigate to http://127.0.0.1:9000

Faber:
Enter in field
```
Wallet Seed:  0123456789ABCDEF0123456789ABCDEF
```
Press ```Register DID```

Output:

```
Seed: 0123456789ABCDEF0123456789ABCDEF
DID: 3avoBCqDMFHFaKUHug9s8W
Verkey: 2QiWG18JjfjUFQMk8xdmhyphRzmbveaYbGM3R8iPbiBx
```

Note DID is same as ledger NYM in the associated transaction
Takes a few seconds for the ledger to show new transaction.
Go to Domain link on page

Ledger Transaction:

```
#10
Message Wrapper
Root hash: HgxLc6h6R12P5zSM1h7T5jSttmAoHryhmrshffmM9imx
Audit path: Gk2Q86RBUx7o6EHYm8snDMJuBKS7cVG66T88NW3GB7bV, DNHM372JZJoGcxdHdmsj3QSSiomyeZux6ssJXxAJqyvd
Metadata
From nym: V4SGRU86Z58d6TV7PBUe6f
Transaction
Type: NYM
Nym: 462p8mtcX6jpa9ky565YEL
Role: (none)
Verkey: ~LCgq4hnSvMvB8nKd9vgsTD
Raw Data
```

## 4) Run web hook server leopy

See readme at https://github.com/SmithSamuelM/leopy


To use pip install

```bash
$ pip3 install leopy
```

Then from command line

```bash
$ leopyd -v 1
```

For help

```bash
$ leopyd -h

usage: leopyd [-h] [-V] [-v VERBOSE] [-P PORT]

Runs leopy controller server. Example: app.py --port 8080'

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Prints out version of script runner.
  -v VERBOSE, --verbose VERBOSE
                        Verbosity level.
  -P PORT, --port PORT  Port number the server should listen on. Default is
                        8080.

```

Or run from cloned repo

```bash
$ cd /.../leopy/src/
$ python3 -m leopy.leopyd -v 1
```

If starts up correctly should see on console

```
----------------------
Starting mission plan 'main.flo' from file:
    /usr/local/lib/python3.7/site-packages/leopy/flo/main.flo
Starting Skedder 'skedder' ...
   Starting Framer 'leopy' ...
To: leopy<<leopy> at 0.0
*** Starting Server ***
   Starting Framer 'server' ...
To: server<<server> at 0.0
IP Address ('', 8080)
```

Console will also show SSE stream of events received by webhook controller
from aca-py agent.

To see to see SSE stream of events sent by Agent to Controller in a broswer
Navigate browser to

```
http://localhost:8080/events
```



## 5) Run aca-py CLI for Faber Agent with controller

If restarted Indy ledger pool need to clean wallets to start with empty wallet.

```bash
$ cd ~/.indy_client/wallet
$ rm -r agent_faber*
```

Need to find out what ```~/.indy_client/wallet/trustee_wallet/``` is used for.

To get list of command line options.

```bash
$ aca-py start --help
```


Faber with webhook controller

```bash
$ aca-py start \
--inbound-transport http 0.0.0.0 8020 \
--outbound-transport http \
--log-level debug \
--debug-connections \
--debug-credentials \
--debug-presentations \
--endpoint http://localhost:8020 \
--label FaberAgent  \
--seed 0123456789ABCDEF0123456789ABCDEF \
--ledger-pool-name localindypool \
--admin 0.0.0.0 8021 \
--admin-insecure-mode \
--auto-ping-connection \
--public-invites \
--auto-accept-invites \
--auto-accept-requests \
--auto-respond-messages \
--auto-respond-credential-offer \
--auto-respond-presentation-request \
--auto-store-credential \
--auto-verify-presentation \
--wallet-key agent_faber \
--wallet-name agent_faber \
--wallet-type indy \
--genesis-url http://localhost:9000/genesis \
--webhook-url http://localhost:8080
```

If it runs successfully the console should eventually print out the following:

```bash
::::::::::::::::::::::::::::::::::::::::::::::
:: Aries Cloud Agent                        ::
::                                          ::
::                                          ::
:: Inbound Transports:                      ::
::                                          ::
::   - http://0.0.0.0:8020                  ::
::                                          ::
:: Outbound Transports:                     ::
::                                          ::
::   - http                                 ::
::   - https                                ::
::                                          ::
:: Public DID Information:                  ::
::                                          ::
::   - DID: 3avoBCqDMFHFaKUHug9s8W          ::
::                                          ::
:: Administration API:                      ::
::                                          ::
::   - http://0.0.0.0:8021                  ::
::                                          ::
::                               ver: 0.3.1 ::
::::::::::::::::::::::::::::::::::::::::::::::

Listening...

```

Faber's Swagger interface is at ```http://127.0.0.1:8021/```
This is defined by the ```--admin 0.0.0.0 8021``` option above.





## 6) Create Schema by Faber


Swagger Faber

```
POST /schemas  Sends a schema to the ledger
```

```json
{
  "schema_name": "fabername",
  "schema_version": "0.1.0",
  "attributes":
  [
    "name"
  ]
}
```

Response:
```json
{
  "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0"
}
```

schema_id is same as ledger transaction id

No Webhook events

Ledger:
Creates 3 ledger transactions: Two ATTRIB and one SCHEMA


Ledger Transactions:

```
#11
Message Wrapper
Transaction ID: 8e2cd66a244f6e9f282882168b085d235ecb162e7166693f750f62c219bc245c
Transaction time: 9/9/2019, 2:37:07 PM (1568061427)
Signed by: V4SGRU86Z58d6TV7PBUe6f
Root hash: ALQgekVMPmibqeRdXqSumbpxdvLGVCqjr31g94pUFLWL
Audit path: EsY4hbw8MPXuyQTiq43pvwJqak6pGzfKwJKMXoi6uYS7, DNHM372JZJoGcxdHdmsj3QSSiomyeZux6ssJXxAJqyvd
Metadata
From nym: V4SGRU86Z58d6TV7PBUe6f
Request ID: 1568061427799680000
Digest: 7ca2396293ad99a6898af5b59311d395fbd2ed5b7fa3c113b15457468b0b23d3
Transaction
Type: NYM
Nym: 3avoBCqDMFHFaKUHug9s8W
Role: TRUST_ANCHOR
Verkey: 2QiWG18JjfjUFQMk8xdmhyphRzmbveaYbGM3R8iPbiBx
Raw Data
#12
Message Wrapper
Transaction ID: 3avoBCqDMFHFaKUHug9s8W:1:b6bf7bc8d96f3ea9d132c83b3da8e7760e420138485657372db4d6a981d3fd9e
Transaction time: 9/9/2019, 2:46:08 PM (1568061968)
Signed by: 3avoBCqDMFHFaKUHug9s8W
Root hash: 8nhNq8nd2bkbTpPwRUDNzRRtAa1LdSKWksBT5E21BbUy
Audit path: GLuikYGe44b7PNG5itSz2qU2HHucDL7Jb1TqPvEjWCyA, EsY4hbw8MPXuyQTiq43pvwJqak6pGzfKwJKMXoi6uYS7, DNHM372JZJoGcxdHdmsj3QSSiomyeZux6ssJXxAJqyvd
Metadata
From nym: 3avoBCqDMFHFaKUHug9s8W
Request ID: 1568061968417855000
Digest: f3dfb6b568337f8a81d4914028b28d50521dcdf479af9b1d4562c629a1a0ce14
Transaction
Type: ATTRIB
Nym: 3avoBCqDMFHFaKUHug9s8W
Attribute data: {"endpoint":{"endpoint":"http://localhost:8020"}}
Raw Data
#13
Message Wrapper
Transaction ID: 3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0
Transaction time: 9/9/2019, 2:47:40 PM (1568062060)
Signed by: 3avoBCqDMFHFaKUHug9s8W
Root hash: DeM44Ts9f1xAK9fJYdGZeMskBrRt1y16Lx5SaCpYCmr2
Audit path: ADCk1fhGzS3JacoBog3DKaM41v2wsWWJgjXJwq4q6m3f, DNHM372JZJoGcxdHdmsj3QSSiomyeZux6ssJXxAJqyvd
Metadata
From nym: 3avoBCqDMFHFaKUHug9s8W
Request ID: 1568062060601032000
Digest: bbf193ba0b9bc1e0ada136cb7051b74789e9eef44f5a5d819c1914ec893a2a82
Transaction
Type: SCHEMA
Schema name: fabername
Schema version: 0.1.0
Schema attributes:
name
Raw Data
```

## 7) Register Credential Definition by Faber


Faber
```POST /credential-definitions   Sends a credential definition to the ledger```

```json
{
  "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0"
}
```

Response :

```json
{
  "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
}

```

Cred Def ID and ledger transaction id are the same.
Notice that schema trans number 15 (below) is in the cred def id.

No webhook events

Ledger Transaction

```
#14
Message Wrapper
Transaction ID: 3avoBCqDMFHFaKUHug9s8W:3:CL:13:default
Transaction time: 9/9/2019, 2:50:13 PM (1568062213)
Signed by: 3avoBCqDMFHFaKUHug9s8W
Root hash: GFCq6DNhwZssoqNt2e4NADTdWv4bMghqNmLZdFFYvf2h
Audit path: 5ExauSdq7tXoVPnTmReBRjfX33CNzmy34w4EoiHn7Lvt, ADCk1fhGzS3JacoBog3DKaM41v2wsWWJgjXJwq4q6m3f, DNHM372JZJoGcxdHdmsj3QSSiomyeZux6ssJXxAJqyvd
Metadata
From nym: 3avoBCqDMFHFaKUHug9s8W
Request ID: 1568062213175658000
Digest: 9351f27682b9c90ec02cf000c1045d511e88a0ea89429cc3796e7dd904e3b7cc
Transaction
Type: CRED_DEF
Reference: 13
Signature type: CL
Tag: default
Attributes:
master_secret
name
Raw Data
```

### Notes

OK, the one time setup work for issuing a credential complete.
We can now issue 1 or a million credentials without having to do those steps again.
Astute readers might note that we did not setup a revocation registry,
so we cannot revoke the credentials we issue with that credential definition.
You can’t have everything in an easy demo (and we’re still working on enabling that).



## 8) Create Connection invitation from Faber

Using swagger to create invitation on Faber's admin interface :8021

Faber
```
POST /connections/create-invitation  Create a new connection invitation
```


Response body:

```json
{
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "invitation": {
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
    "@id": "1fec9664-4b44-443b-b55c-012cc1e3aa47",
    "serviceEndpoint": "http://localhost:8020",
    "recipientKeys": [
      "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf"
    ],
    "label": "FaberAgent"
  },
  "invitation_url": "http://localhost:8020?c_i=eyJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9jb25uZWN0aW9ucy8xLjAvaW52aXRhdGlvbiIsICJAaWQiOiAiMWZlYzk2NjQtNGI0NC00NDNiLWI1NWMtMDEyY2MxZTNhYTQ3IiwgInNlcnZpY2VFbmRwb2ludCI6ICJodHRwOi8vbG9jYWxob3N0OjgwMjAiLCAicmVjaXBpZW50S2V5cyI6IFsiOExITXN2WWlkUHZyaDFpckZzV0plUlF3QURrV1ZBTjFFR2ZYQ0hXcE1iTGYiXSwgImxhYmVsIjogIkZhYmVyQWdlbnQifQ=="
}
```


Invitation
```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
    "@id": "1fec9664-4b44-443b-b55c-012cc1e3aa47",
    "serviceEndpoint": "http://localhost:8020",
    "recipientKeys": [
      "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf"
    ],
    "label": "FaberAgent"
  }
```

Faber Webhook Events:

```json
Sink: /topic/connections/ POST
JSON:
```
```json
{
  "topic": "connections",
  "data": {
    "state": "invitation",
    "initiator": "self",
    "created_at": "2019-09-09 20:52:23.691890Z",
    "invitation_mode": "once",
    "routing_state": "none",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "accept": "auto",
    "invitation_key": "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf",
    "updated_at": "2019-09-09 20:52:23.691890Z"
  }
}


```

## 9) Use von-network browser to create public DID for Alice.

Not sure if Alice needs a public DID. When running the Alice Agent we pass
in a seed for DID but if Alice does not create schema or cred def does alice need Public DID
If so do we not pass in seed to alice agent.


Navigate to http://127.0.0.1:9000

Alice:
Enter in field

```Wallet Seed:  ABCDEF0123456789ABCDEF0123456789```

Output
```
Seed: ABCDEF0123456789ABCDEF0123456789
DID: KfoDwEpcJoNCdb6Akeeb9w
Verkey: BBAM5UQdhfFvSdihv4SbEcV3zAyLZ2dEs3WwBnh2cHw2
```

Note DID is same as ledger NYM

Ledger Transaction

```
#15
Message Wrapper
Transaction ID: 362ee23b301ecd06537351528d9e44b824ab69974f158f9b2fef1d55e0ec9dbe
Transaction time: 9/9/2019, 2:53:42 PM (1568062422)
Signed by: V4SGRU86Z58d6TV7PBUe6f
Root hash: CVvLT5QyngjduGLxfMg9aT4abnTvry6VEDoPKba8xwmu
Audit path: 6xdMz4Vh49WBxuNd9bPCwMzPbnjPSVJ7Lb2huoLP8F4i, ADCk1fhGzS3JacoBog3DKaM41v2wsWWJgjXJwq4q6m3f, DNHM372JZJoGcxdHdmsj3QSSiomyeZux6ssJXxAJqyvd
Metadata
From nym: V4SGRU86Z58d6TV7PBUe6f
Request ID: 1568062422114503000
Digest: b26b1f8bcd07a9e44363a96b943d638f0a21e39c0ff5163cbba15cb73165c6cf
Transaction
Type: NYM
Nym: KfoDwEpcJoNCdb6Akeeb9w
Role: TRUST_ANCHOR
Verkey: BBAM5UQdhfFvSdihv4SbEcV3zAyLZ2dEs3WwBnh2cHw2
Raw Data
```





## 10) Run aca-py CLI for Alice Agent without controller

If restarted Indy ledger pool need to clean wallets to start with empty wallet.

```bash
$ cd ~/.indy_client/wallet
$ rm -r agent_alice*
```

To get list of command line options.

```bash
$ aca-py start --help
```


Alice without controller

```bash
$ aca-py start \
--inbound-transport http 0.0.0.0 8030 \
--outbound-transport http \
--log-level debug \
--debug-connections \
--debug-credentials \
--debug-presentations \
--endpoint http://localhost:8030 \
--label AliceAgent \
--seed ABCDEF0123456789ABCDEF0123456789 \
--ledger-pool-name localindypool \
--admin 0.0.0.0 8031 \
--admin-insecure-mode \
--auto-ping-connection \
--public-invites \
--auto-accept-invites \
--auto-accept-requests \
--auto-respond-messages \
--auto-respond-credential-offer \
--auto-respond-presentation-request \
--auto-store-credential \
--auto-verify-presentation \
--wallet-key agent_alice \
--wallet-name agent_alice \
--wallet-type indy \
--genesis-url http://localhost:9000/genesis
```

If it runs successfully the console should eventually print out the following:

```bash
::::::::::::::::::::::::::::::::::::::::::::::
:: Aries Cloud Agent                        ::
::                                          ::
::                                          ::
:: Inbound Transports:                      ::
::                                          ::
::   - http://0.0.0.0:8030                  ::
::                                          ::
:: Outbound Transports:                     ::
::                                          ::
::   - http                                 ::
::   - https                                ::
::                                          ::
:: Public DID Information:                  ::
::                                          ::
::   - DID: KfoDwEpcJoNCdb6Akeeb9w          ::
::                                          ::
:: Administration API:                      ::
::                                          ::
::   - http://0.0.0.0:8031                  ::
::                                          ::
::                               ver: 0.3.1 ::
::::::::::::::::::::::::::::::::::::::::::::::

Listening...



```

Alices's Swagger interface is at
```http://127.0.0.1:8031/```
This is defined by the ```--admin 0.0.0.0 8031``` option above.




## 11) Receive Connection invitation from Faber at Alice

Copy the entire block of the invitation object, from the curly brackets {},
excluding the trailing comma.

Go to Alice's Swagger :8031 and receive the invitation
Copy invitation from Faber response above

```
POST /connections/receive-invitation Receive a new connection invitation
```

Invitation:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
    "@id": "1fec9664-4b44-443b-b55c-012cc1e3aa47",
    "serviceEndpoint": "http://localhost:8020",
    "recipientKeys": [
      "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf"
    ],
    "label": "FaberAgent"
  }

```

Response:
```json
{
  "created_at": "2019-09-09 20:56:50.507932Z",
  "their_label": "FaberAgent",
  "routing_state": "none",
  "initiator": "external",
  "invitation_key": "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf",
  "connection_id": "2d67c0a7-3c07-426c-b28f-89fec182f308",
  "request_id": "675feb2e-a521-40a0-a566-bf98f52c1f08",
  "state": "request",
  "updated_at": "2019-09-09 20:56:50.522666Z",
  "invitation_mode": "once",
  "accept": "auto",
  "my_did": "USz54LX588nXZzvJZaaauo"
}
```

Faber Events Webhook:


```Sink: /topic/connections/ POST```
```json
{
  "topic": "connections",
  "data": {
    "state": "request",
    "initiator": "self",
    "created_at": "2019-09-09 20:52:23.691890Z",
    "their_label": "AliceAgent",
    "invitation_mode": "once",
    "routing_state": "none",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "accept": "auto",
    "their_did": "USz54LX588nXZzvJZaaauo",
    "invitation_key": "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf",
    "updated_at": "2019-09-09 20:56:50.609525Z"
  }
}
```
Sink: /topic/connections/ POST
JSON:
```
```json
{
  "topic": "connections",
  "data": {
    "state": "response",
    "initiator": "self",
    "created_at": "2019-09-09 20:52:23.691890Z",
    "their_label": "AliceAgent",
    "invitation_mode": "once",
    "my_did": "QGBGeR9rrnzY9FqnzMpmgy",
    "routing_state": "none",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "accept": "auto",
    "their_did": "USz54LX588nXZzvJZaaauo",
    "invitation_key": "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf",
    "updated_at": "2019-09-09 20:56:50.637371Z"
  }
}
```

```
Sink: /topic/connections/ POST
JSON:

```
```json
{
  "topic": "connections",
  "data": {
    "state": "active",
    "initiator": "self",
    "created_at": "2019-09-09 20:52:23.691890Z",
    "their_label": "AliceAgent",
    "invitation_mode": "once",
    "my_did": "QGBGeR9rrnzY9FqnzMpmgy",
    "routing_state": "none",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "accept": "auto",
    "their_did": "USz54LX588nXZzvJZaaauo",
    "invitation_key": "8LHMsvYidPvrh1irFsWJeRQwADkWVAN1EGfXCHWpMbLf",
    "updated_at": "2019-09-09 20:56:50.757535Z"
  }
}```





### Connection Success

```
Faber: "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123"
Alice: "connection_id": "2d67c0a7-3c07-426c-b28f-89fec182f308"
```


## 10) Issue Credential from Faber to Alice

Faber to Alice

```POST /credential_exchange/send    Sends a credential and automates the entire flow```

Use Faber's connection id with Alice and the cred def id from above.
Credential is just a name string. Not very interesting but basic.

```json
{
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
  "credential_values": {"name": "Alice Jones"}
}
```

Response:
```json

{
  "credential_values": {
    "name": "Alice Jones"
  },
  "updated_at": "2019-09-09 21:00:08.402126Z",
  "auto_issue": true,
  "initiator": "self",
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
  "credential_offer": {
    "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
    "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
    "key_correctness_proof": {
      "c": "50452586530256478209972482632580110767479945289195765941464134003203365225451",
      "xz_cap": "973607954881487358409273087321964720746871162072952177510913234187297225927280855876252151723441411119320043048834816731831213118923767295637785328896761927231897869714139924181121139716060647124476293702710706626713799680288189135217694772391294355295763398519489385683269095653779169047626089990592755512215817359873006828466715349337571162497294317947442321981271120472080778408559215113359921045399188842541820233947817032831827915582902344344113362431152901202437219941785842401853044415888944100501504066520446792648451374624708105995874072359559009927906066114973451692139131088613711167263382544913691523935665743016758255693298414556640012103903148236259339227939350769101437637339140",
      "xr_cap": [
        [
          "name",
          "26798455675766069403184519115903594233992716212390730441572334433630608847896249485252296730702038931435627546540714507061238374324995645094446260826095074517365040323439514918204835166482957607417116126966553798324055153249769285654857636816258873005585623042169792981119262363012857359507934735548766219977295748915134655218695198942004631766425410067003935605224740460854512670653015604445145614014551609498842622890192201205706550469635689759240808145135676280461601163143742246459867239052757867404968369610163351718544659474531578450004192827803415123454459870270520025980739847419930404938771331496356860988931747715442841020191891338025636243657408236839319190943456415728472643849222"
        ],
        [
          "master_secret",
          "1181475898038686351837196807352260845792801338560348802225149492527896370695252704287349701511167948567961120880288320355270212294577996090842505479923199773604638919023308885419067358554139319016902725173490988742266251681275571874764738771274669216077561313806226538433115375187404580921408396690027380571192225608915216168283518249134259952479687900295750395850822109513325985713237268408564593531388801813955320980120456025785676224929876080389189419540921270896707582831627571936551494271264820451553633290732259448481250779194466644089572566611376313515729142299957059058342156963583647683569160567389665882663010526927571779729628949366807560576357915012024388090512433850067178423500543"
        ]
      ]
    },
    "nonce": "759715947375168567892402"
  },
  "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
  "state": "offer_sent",
  "created_at": "2019-09-09 21:00:08.402126Z",
  "credential_exchange_id": "2bbcb44b-cb28-4f89-b3ac-87849be146eb"
}

```

Faber Webhook Events:

```
Sink: /topic/credentials/ POST
JSON:
```

```json
{
  "topic": "credentials",
  "data": {
    "credential_values": {
      "name": "Alice Jones"
    },
    "updated_at": "2019-09-09 21:00:08.402126Z",
    "auto_issue": true,
    "initiator": "self",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
    "credential_offer": {
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "key_correctness_proof": {
        "c": "50452586530256478209972482632580110767479945289195765941464134003203365225451",
        "xz_cap": "973607954881487358409273087321964720746871162072952177510913234187297225927280855876252151723441411119320043048834816731831213118923767295637785328896761927231897869714139924181121139716060647124476293702710706626713799680288189135217694772391294355295763398519489385683269095653779169047626089990592755512215817359873006828466715349337571162497294317947442321981271120472080778408559215113359921045399188842541820233947817032831827915582902344344113362431152901202437219941785842401853044415888944100501504066520446792648451374624708105995874072359559009927906066114973451692139131088613711167263382544913691523935665743016758255693298414556640012103903148236259339227939350769101437637339140",
        "xr_cap": [
          [
            "name",
            "26798455675766069403184519115903594233992716212390730441572334433630608847896249485252296730702038931435627546540714507061238374324995645094446260826095074517365040323439514918204835166482957607417116126966553798324055153249769285654857636816258873005585623042169792981119262363012857359507934735548766219977295748915134655218695198942004631766425410067003935605224740460854512670653015604445145614014551609498842622890192201205706550469635689759240808145135676280461601163143742246459867239052757867404968369610163351718544659474531578450004192827803415123454459870270520025980739847419930404938771331496356860988931747715442841020191891338025636243657408236839319190943456415728472643849222"
          ],
          [
            "master_secret",
            "1181475898038686351837196807352260845792801338560348802225149492527896370695252704287349701511167948567961120880288320355270212294577996090842505479923199773604638919023308885419067358554139319016902725173490988742266251681275571874764738771274669216077561313806226538433115375187404580921408396690027380571192225608915216168283518249134259952479687900295750395850822109513325985713237268408564593531388801813955320980120456025785676224929876080389189419540921270896707582831627571936551494271264820451553633290732259448481250779194466644089572566611376313515729142299957059058342156963583647683569160567389665882663010526927571779729628949366807560576357915012024388090512433850067178423500543"
          ]
        ]
      },
      "nonce": "759715947375168567892402"
    },
    "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
    "state": "offer_sent",
    "created_at": "2019-09-09 21:00:08.402126Z",
    "credential_exchange_id": "2bbcb44b-cb28-4f89-b3ac-87849be146eb"
  }
}

```
```
Sink: /topic/credentials/ POST
JSON:
```
```json
{
  "topic": "credentials",
  "data": {
    "credential_values": {
      "name": "Alice Jones"
    },
    "updated_at": "2019-09-09 21:00:10.072797Z",
    "auto_issue": true,
    "initiator": "self",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "thread_id": "db475c51-0630-4fbd-9ddb-28c7676f1fad",
    "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
    "credential_request": {
      "prover_did": "USz54LX588nXZzvJZaaauo",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "blinded_ms": {
        "u": "99368895797536005994311578723189357674473888721194302817275899605659815579082776035889727937509149843902587581396694097380001137952451816178530770768521813901129081437176205941944065200271520024859963251064451377398768846912432396109867523131209543363488226760277539406928453777223625182259241308969628882540671093876658006934832956644288049409819530272004889072620189012294592330334635260630961922620635703716969003181853188178982291121888203909561688206211503826185916253632379861409156552241548354871543971458468129569412836309227637169916178695946550538097767138914450365505044802717690371144577045034596177069218",
        "ur": null,
        "hidden_attributes": [
          "master_secret"
        ],
        "committed_attributes": {}
      },
      "blinded_ms_correctness_proof": {
        "c": "82814368957593600542678573704265961728440515441532250993783760615697056042766",
        "v_dash_cap": "2118452362398745861280226057596824191481494477242721958942324742953084725675464959425613275439996307006090128873526174900550688825200704332952595267412793247827461612669522329485045242589005220163235341676269260760388476609945675148280360463542384583398853903862359134202158782311554154739994184363677101683603079599084416381670111627232980638055599465177598913645868266764089443449862992176864925745186449013730471429866771461184116930725948848731317657299234761870227355190066369188033430582072763347201781851825566140580053014392699389990683680999169805660350968648440532935808946668533750546941833754340355282870786638599282983773855233579000116239048351315802722580655134903452234145646701421420006720424362392380",
        "m_caps": {
          "master_secret": "24225459579209831479420816101972689886146719984334583846534574626255831902742393762937117009729103049145090884891989587187027426846285733606614192343459832623110571090085221331919"
        },
        "r_caps": {}
      },
      "nonce": "1019073401153768641589280"
    },
    "credential_offer": {
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "key_correctness_proof": {
        "c": "50452586530256478209972482632580110767479945289195765941464134003203365225451",
        "xz_cap": "973607954881487358409273087321964720746871162072952177510913234187297225927280855876252151723441411119320043048834816731831213118923767295637785328896761927231897869714139924181121139716060647124476293702710706626713799680288189135217694772391294355295763398519489385683269095653779169047626089990592755512215817359873006828466715349337571162497294317947442321981271120472080778408559215113359921045399188842541820233947817032831827915582902344344113362431152901202437219941785842401853044415888944100501504066520446792648451374624708105995874072359559009927906066114973451692139131088613711167263382544913691523935665743016758255693298414556640012103903148236259339227939350769101437637339140",
        "xr_cap": [
          [
            "name",
            "26798455675766069403184519115903594233992716212390730441572334433630608847896249485252296730702038931435627546540714507061238374324995645094446260826095074517365040323439514918204835166482957607417116126966553798324055153249769285654857636816258873005585623042169792981119262363012857359507934735548766219977295748915134655218695198942004631766425410067003935605224740460854512670653015604445145614014551609498842622890192201205706550469635689759240808145135676280461601163143742246459867239052757867404968369610163351718544659474531578450004192827803415123454459870270520025980739847419930404938771331496356860988931747715442841020191891338025636243657408236839319190943456415728472643849222"
          ],
          [
            "master_secret",
            "1181475898038686351837196807352260845792801338560348802225149492527896370695252704287349701511167948567961120880288320355270212294577996090842505479923199773604638919023308885419067358554139319016902725173490988742266251681275571874764738771274669216077561313806226538433115375187404580921408396690027380571192225608915216168283518249134259952479687900295750395850822109513325985713237268408564593531388801813955320980120456025785676224929876080389189419540921270896707582831627571936551494271264820451553633290732259448481250779194466644089572566611376313515729142299957059058342156963583647683569160567389665882663010526927571779729628949366807560576357915012024388090512433850067178423500543"
          ]
        ]
      },
      "nonce": "759715947375168567892402"
    },
    "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
    "state": "request_received",
    "created_at": "2019-09-09 21:00:08.402126Z",
    "credential_exchange_id": "2bbcb44b-cb28-4f89-b3ac-87849be146eb"
  }
}
```
```
Sink: /topic/credentials/ POST
JSON:
```
```json
{
  "topic": "credentials",
  "data": {
    "credential_values": {
      "name": "Alice Jones"
    },
    "updated_at": "2019-09-09 21:00:10.611065Z",
    "auto_issue": true,
    "initiator": "self",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "credential": {
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "rev_reg_id": null,
      "values": {
        "name": {
          "raw": "Alice Jones",
          "encoded": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
        }
      },
      "signature": {
        "p_credential": {
          "m_2": "57832835556928742723946725004638238236382427793876617639158517726445069815397",
          "a": "20335594316731334597758816443885619716281946894071547670112874227353349613733788033617671091848119624077343554670947282810485774124636153228333825818186760397527729892806528284243491342499262911619541896964620427749043381625203893661466943880747122017539322865930800203806065857795584699623987557173946111100450130555197585324032975907705976283592876161733661021481170756352943172201881541765527633833412431874555779986196454199886878078859992928382512010526711165717317294021035408585595567390933051546616905350933492259317172537982279278238456869493798937355032304448696707549688520575565393297998400926856935054785",
          "e": "259344723055062059907025491480697571938277889515152306249728583105665800713306759149981690559193987143012367913206299323899696942213235956742930114221280625468933785621106476195767",
          "v": "6264315754962089362691677910875768714719628097173834826942639456162861264780209679632476338104728648674666095282910717315628966174111516324733617604883927936031834134944562245348356595475949760140820205017843765225176947252534891385340037654527825604373031641665762232119470199172203915071879260274922482308419475927587898260844045340005759709509719230224917577081434498505999519246994431019808643717455525020238858900077950802493426663298211783820016830018445034267920428147219321200498121844471986156393710041532347890155773933440967485292509669092990420513062430659637641764166558511575862600071368439136343180394499313466692464923385392375334511727761876368691568580574716011747008456027092663180661749027223129454567715456876258225945998241007751462618767907499044716919115655029979467845162863204339002632523083819"
        },
        "r_credential": null
      },
      "signature_correctness_proof": {
        "se": "16380378819766384687299800964395104347426132415600670073499502988403571039552426989440730562439872799389359320216622430122149635890650280073919616970308875713611769602805907315796100888051513191790990723115153015179238215201014858697020476301190889292739142646098613335687696678474499610035829049097552703970387216872374849734708764603376911608392816067509505173513379900549958002287975424637744258982508227210821445545063280589183914569333870632968595659796744088289167771635644102920825749994200219186110532662348311959247565066406030309945998501282244986323336410628720691577720308242032279888024250179409222261839",
        "c": "54687071895183924055442269144489786903186459631877792294627879136747836413523"
      },
      "rev_reg": null,
      "witness": null
    },
    "thread_id": "db475c51-0630-4fbd-9ddb-28c7676f1fad",
    "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
    "credential_request": {
      "prover_did": "USz54LX588nXZzvJZaaauo",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "blinded_ms": {
        "u": "99368895797536005994311578723189357674473888721194302817275899605659815579082776035889727937509149843902587581396694097380001137952451816178530770768521813901129081437176205941944065200271520024859963251064451377398768846912432396109867523131209543363488226760277539406928453777223625182259241308969628882540671093876658006934832956644288049409819530272004889072620189012294592330334635260630961922620635703716969003181853188178982291121888203909561688206211503826185916253632379861409156552241548354871543971458468129569412836309227637169916178695946550538097767138914450365505044802717690371144577045034596177069218",
        "ur": null,
        "hidden_attributes": [
          "master_secret"
        ],
        "committed_attributes": {}
      },
      "blinded_ms_correctness_proof": {
        "c": "82814368957593600542678573704265961728440515441532250993783760615697056042766",
        "v_dash_cap": "2118452362398745861280226057596824191481494477242721958942324742953084725675464959425613275439996307006090128873526174900550688825200704332952595267412793247827461612669522329485045242589005220163235341676269260760388476609945675148280360463542384583398853903862359134202158782311554154739994184363677101683603079599084416381670111627232980638055599465177598913645868266764089443449862992176864925745186449013730471429866771461184116930725948848731317657299234761870227355190066369188033430582072763347201781851825566140580053014392699389990683680999169805660350968648440532935808946668533750546941833754340355282870786638599282983773855233579000116239048351315802722580655134903452234145646701421420006720424362392380",
        "m_caps": {
          "master_secret": "24225459579209831479420816101972689886146719984334583846534574626255831902742393762937117009729103049145090884891989587187027426846285733606614192343459832623110571090085221331919"
        },
        "r_caps": {}
      },
      "nonce": "1019073401153768641589280"
    },
    "credential_offer": {
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "key_correctness_proof": {
        "c": "50452586530256478209972482632580110767479945289195765941464134003203365225451",
        "xz_cap": "973607954881487358409273087321964720746871162072952177510913234187297225927280855876252151723441411119320043048834816731831213118923767295637785328896761927231897869714139924181121139716060647124476293702710706626713799680288189135217694772391294355295763398519489385683269095653779169047626089990592755512215817359873006828466715349337571162497294317947442321981271120472080778408559215113359921045399188842541820233947817032831827915582902344344113362431152901202437219941785842401853044415888944100501504066520446792648451374624708105995874072359559009927906066114973451692139131088613711167263382544913691523935665743016758255693298414556640012103903148236259339227939350769101437637339140",
        "xr_cap": [
          [
            "name",
            "26798455675766069403184519115903594233992716212390730441572334433630608847896249485252296730702038931435627546540714507061238374324995645094446260826095074517365040323439514918204835166482957607417116126966553798324055153249769285654857636816258873005585623042169792981119262363012857359507934735548766219977295748915134655218695198942004631766425410067003935605224740460854512670653015604445145614014551609498842622890192201205706550469635689759240808145135676280461601163143742246459867239052757867404968369610163351718544659474531578450004192827803415123454459870270520025980739847419930404938771331496356860988931747715442841020191891338025636243657408236839319190943456415728472643849222"
          ],
          [
            "master_secret",
            "1181475898038686351837196807352260845792801338560348802225149492527896370695252704287349701511167948567961120880288320355270212294577996090842505479923199773604638919023308885419067358554139319016902725173490988742266251681275571874764738771274669216077561313806226538433115375187404580921408396690027380571192225608915216168283518249134259952479687900295750395850822109513325985713237268408564593531388801813955320980120456025785676224929876080389189419540921270896707582831627571936551494271264820451553633290732259448481250779194466644089572566611376313515729142299957059058342156963583647683569160567389665882663010526927571779729628949366807560576357915012024388090512433850067178423500543"
          ]
        ]
      },
      "nonce": "759715947375168567892402"
    },
    "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
    "state": "issued",
    "created_at": "2019-09-09 21:00:08.402126Z",
    "credential_exchange_id": "2bbcb44b-cb28-4f89-b3ac-87849be146eb"
  }
}
```
```
Sink: /topic/credentials/ POST
JSON:
```

```json
{
  "topic": "credentials",
  "data": {
    "credential_values": {
      "name": "Alice Jones"
    },
    "updated_at": "2019-09-09 21:00:10.725006Z",
    "auto_issue": true,
    "initiator": "self",
    "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
    "credential": {
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "rev_reg_id": null,
      "values": {
        "name": {
          "raw": "Alice Jones",
          "encoded": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
        }
      },
      "signature": {
        "p_credential": {
          "m_2": "57832835556928742723946725004638238236382427793876617639158517726445069815397",
          "a": "20335594316731334597758816443885619716281946894071547670112874227353349613733788033617671091848119624077343554670947282810485774124636153228333825818186760397527729892806528284243491342499262911619541896964620427749043381625203893661466943880747122017539322865930800203806065857795584699623987557173946111100450130555197585324032975907705976283592876161733661021481170756352943172201881541765527633833412431874555779986196454199886878078859992928382512010526711165717317294021035408585595567390933051546616905350933492259317172537982279278238456869493798937355032304448696707549688520575565393297998400926856935054785",
          "e": "259344723055062059907025491480697571938277889515152306249728583105665800713306759149981690559193987143012367913206299323899696942213235956742930114221280625468933785621106476195767",
          "v": "6264315754962089362691677910875768714719628097173834826942639456162861264780209679632476338104728648674666095282910717315628966174111516324733617604883927936031834134944562245348356595475949760140820205017843765225176947252534891385340037654527825604373031641665762232119470199172203915071879260274922482308419475927587898260844045340005759709509719230224917577081434498505999519246994431019808643717455525020238858900077950802493426663298211783820016830018445034267920428147219321200498121844471986156393710041532347890155773933440967485292509669092990420513062430659637641764166558511575862600071368439136343180394499313466692464923385392375334511727761876368691568580574716011747008456027092663180661749027223129454567715456876258225945998241007751462618767907499044716919115655029979467845162863204339002632523083819"
        },
        "r_credential": null
      },
      "signature_correctness_proof": {
        "se": "16380378819766384687299800964395104347426132415600670073499502988403571039552426989440730562439872799389359320216622430122149635890650280073919616970308875713611769602805907315796100888051513191790990723115153015179238215201014858697020476301190889292739142646098613335687696678474499610035829049097552703970387216872374849734708764603376911608392816067509505173513379900549958002287975424637744258982508227210821445545063280589183914569333870632968595659796744088289167771635644102920825749994200219186110532662348311959247565066406030309945998501282244986323336410628720691577720308242032279888024250179409222261839",
        "c": "54687071895183924055442269144489786903186459631877792294627879136747836413523"
      },
      "rev_reg": null,
      "witness": null
    },
    "thread_id": "db475c51-0630-4fbd-9ddb-28c7676f1fad",
    "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
    "credential_request": {
      "prover_did": "USz54LX588nXZzvJZaaauo",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "blinded_ms": {
        "u": "99368895797536005994311578723189357674473888721194302817275899605659815579082776035889727937509149843902587581396694097380001137952451816178530770768521813901129081437176205941944065200271520024859963251064451377398768846912432396109867523131209543363488226760277539406928453777223625182259241308969628882540671093876658006934832956644288049409819530272004889072620189012294592330334635260630961922620635703716969003181853188178982291121888203909561688206211503826185916253632379861409156552241548354871543971458468129569412836309227637169916178695946550538097767138914450365505044802717690371144577045034596177069218",
        "ur": null,
        "hidden_attributes": [
          "master_secret"
        ],
        "committed_attributes": {}
      },
      "blinded_ms_correctness_proof": {
        "c": "82814368957593600542678573704265961728440515441532250993783760615697056042766",
        "v_dash_cap": "2118452362398745861280226057596824191481494477242721958942324742953084725675464959425613275439996307006090128873526174900550688825200704332952595267412793247827461612669522329485045242589005220163235341676269260760388476609945675148280360463542384583398853903862359134202158782311554154739994184363677101683603079599084416381670111627232980638055599465177598913645868266764089443449862992176864925745186449013730471429866771461184116930725948848731317657299234761870227355190066369188033430582072763347201781851825566140580053014392699389990683680999169805660350968648440532935808946668533750546941833754340355282870786638599282983773855233579000116239048351315802722580655134903452234145646701421420006720424362392380",
        "m_caps": {
          "master_secret": "24225459579209831479420816101972689886146719984334583846534574626255831902742393762937117009729103049145090884891989587187027426846285733606614192343459832623110571090085221331919"
        },
        "r_caps": {}
      },
      "nonce": "1019073401153768641589280"
    },
    "credential_offer": {
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "key_correctness_proof": {
        "c": "50452586530256478209972482632580110767479945289195765941464134003203365225451",
        "xz_cap": "973607954881487358409273087321964720746871162072952177510913234187297225927280855876252151723441411119320043048834816731831213118923767295637785328896761927231897869714139924181121139716060647124476293702710706626713799680288189135217694772391294355295763398519489385683269095653779169047626089990592755512215817359873006828466715349337571162497294317947442321981271120472080778408559215113359921045399188842541820233947817032831827915582902344344113362431152901202437219941785842401853044415888944100501504066520446792648451374624708105995874072359559009927906066114973451692139131088613711167263382544913691523935665743016758255693298414556640012103903148236259339227939350769101437637339140",
        "xr_cap": [
          [
            "name",
            "26798455675766069403184519115903594233992716212390730441572334433630608847896249485252296730702038931435627546540714507061238374324995645094446260826095074517365040323439514918204835166482957607417116126966553798324055153249769285654857636816258873005585623042169792981119262363012857359507934735548766219977295748915134655218695198942004631766425410067003935605224740460854512670653015604445145614014551609498842622890192201205706550469635689759240808145135676280461601163143742246459867239052757867404968369610163351718544659474531578450004192827803415123454459870270520025980739847419930404938771331496356860988931747715442841020191891338025636243657408236839319190943456415728472643849222"
          ],
          [
            "master_secret",
            "1181475898038686351837196807352260845792801338560348802225149492527896370695252704287349701511167948567961120880288320355270212294577996090842505479923199773604638919023308885419067358554139319016902725173490988742266251681275571874764738771274669216077561313806226538433115375187404580921408396690027380571192225608915216168283518249134259952479687900295750395850822109513325985713237268408564593531388801813955320980120456025785676224929876080389189419540921270896707582831627571936551494271264820451553633290732259448481250779194466644089572566611376313515729142299957059058342156963583647683569160567389665882663010526927571779729628949366807560576357915012024388090512433850067178423500543"
          ]
        ]
      },
      "nonce": "759715947375168567892402"
    },
    "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
    "state": "stored",
    "created_at": "2019-09-09 21:00:08.402126Z",
    "credential_exchange_id": "2bbcb44b-cb28-4f89-b3ac-87849be146eb"
  }
}
```




## 11 Verify Alice Received and Stored Credential

The --auto-store-credential to the CLI start parameters causes Alice to store the credential once issued.



Alice

```GET /credentials  Fetch credentials from wallet```

Response:
```json
{
  "results": [
    {
      "referent": "64ea2e85-c70f-45ad-b609-68bc1ac89816",
      "attrs": {
        "name": "Alice Jones"
      },
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "rev_reg_id": null,
      "cred_rev_id": null
    }
  ]
}
```

Success

```cred_def_id  3avoBCqDMFHFaKUHug9s8W:3:CL:13:default```

Had to dig into credential exchange records to find credential_id field.
This is not the credential_exchange_id nor the cred_def_id.
The get credentials call should return the credential_id not just the cred_def_id
and also the credential_exchange_id


Alice

```GET /credential_exchange  ```



"cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"

"credential_exchange_id": "e4abc052-1425-4a7f-a035-fbec52b77b51"

"credential_id": "64ea2e85-c70f-45ad-b609-68bc1ac89816"


Response:

```json
{
  "results": [
    {
      "created_at": "2019-09-09 21:00:08.467886Z",
      "initiator": "external",
      "credential_exchange_id": "e4abc052-1425-4a7f-a035-fbec52b77b51",
      "credential_request_metadata": {
        "master_secret_blinding_data": {
          "v_prime": "25580734226007719690285673224089715210947756454044468005737391256019498565142900277828263161970182996186273934377468144224418589280534476273301002644723537098259996256214980832953033949208365501976663459087111181218226637532787988416486499994639860563284311361784449952636393479872497215003734667873752681289070725092642969303401464732738277243727348239540903402172112946977399574137004144935286618322490493797841870557760202264035690413808953085389886500399195658320315401651498694433204579401762787752112947921749283570170992743412969155300039316506176676970768595131884581398769852610962798494323860958534023360231914463108896217631928135",
          "vr_prime": null
        },
        "nonce": "1019073401153768641589280",
        "master_secret_name": "agent_alice"
      },
      "credential_offer": {
        "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
        "key_correctness_proof": {
          "c": "50452586530256478209972482632580110767479945289195765941464134003203365225451",
          "xz_cap": "973607954881487358409273087321964720746871162072952177510913234187297225927280855876252151723441411119320043048834816731831213118923767295637785328896761927231897869714139924181121139716060647124476293702710706626713799680288189135217694772391294355295763398519489385683269095653779169047626089990592755512215817359873006828466715349337571162497294317947442321981271120472080778408559215113359921045399188842541820233947817032831827915582902344344113362431152901202437219941785842401853044415888944100501504066520446792648451374624708105995874072359559009927906066114973451692139131088613711167263382544913691523935665743016758255693298414556640012103903148236259339227939350769101437637339140",
          "xr_cap": [
            [
              "name",
              "26798455675766069403184519115903594233992716212390730441572334433630608847896249485252296730702038931435627546540714507061238374324995645094446260826095074517365040323439514918204835166482957607417116126966553798324055153249769285654857636816258873005585623042169792981119262363012857359507934735548766219977295748915134655218695198942004631766425410067003935605224740460854512670653015604445145614014551609498842622890192201205706550469635689759240808145135676280461601163143742246459867239052757867404968369610163351718544659474531578450004192827803415123454459870270520025980739847419930404938771331496356860988931747715442841020191891338025636243657408236839319190943456415728472643849222"
            ],
            [
              "master_secret",
              "1181475898038686351837196807352260845792801338560348802225149492527896370695252704287349701511167948567961120880288320355270212294577996090842505479923199773604638919023308885419067358554139319016902725173490988742266251681275571874764738771274669216077561313806226538433115375187404580921408396690027380571192225608915216168283518249134259952479687900295750395850822109513325985713237268408564593531388801813955320980120456025785676224929876080389189419540921270896707582831627571936551494271264820451553633290732259448481250779194466644089572566611376313515729142299957059058342156963583647683569160567389665882663010526927571779729628949366807560576357915012024388090512433850067178423500543"
            ]
          ]
        },
        "nonce": "759715947375168567892402"
      },
      "credential_definition_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
      "raw_credential": {
        "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
        "rev_reg_id": null,
        "values": {
          "name": {
            "raw": "Alice Jones",
            "encoded": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
          }
        },
        "signature": {
          "p_credential": {
            "m_2": "57832835556928742723946725004638238236382427793876617639158517726445069815397",
            "a": "20335594316731334597758816443885619716281946894071547670112874227353349613733788033617671091848119624077343554670947282810485774124636153228333825818186760397527729892806528284243491342499262911619541896964620427749043381625203893661466943880747122017539322865930800203806065857795584699623987557173946111100450130555197585324032975907705976283592876161733661021481170756352943172201881541765527633833412431874555779986196454199886878078859992928382512010526711165717317294021035408585595567390933051546616905350933492259317172537982279278238456869493798937355032304448696707549688520575565393297998400926856935054785",
            "e": "259344723055062059907025491480697571938277889515152306249728583105665800713306759149981690559193987143012367913206299323899696942213235956742930114221280625468933785621106476195767",
            "v": "6264315754962089362691677910875768714719628097173834826942639456162861264780209679632476338104728648674666095282910717315628966174111516324733617604883927936031834134944562245348356595475949760140820205017843765225176947252534891385340037654527825604373031641665762232119470199172203915071879260274922482308419475927587898260844045340005759709509719230224917577081434498505999519246994431019808643717455525020238858900077950802493426663298211783820016830018445034267920428147219321200498121844471986156393710041532347890155773933440967485292509669092990420513062430659637641764166558511575862600071368439136343180394499313466692464923385392375334511727761876368691568580574716011747008456027092663180661749027223129454567715456876258225945998241007751462618767907499044716919115655029979467845162863204339002632523083819"
          },
          "r_credential": null
        },
        "signature_correctness_proof": {
          "se": "16380378819766384687299800964395104347426132415600670073499502988403571039552426989440730562439872799389359320216622430122149635890650280073919616970308875713611769602805907315796100888051513191790990723115153015179238215201014858697020476301190889292739142646098613335687696678474499610035829049097552703970387216872374849734708764603376911608392816067509505173513379900549958002287975424637744258982508227210821445545063280589183914569333870632968595659796744088289167771635644102920825749994200219186110532662348311959247565066406030309945998501282244986323336410628720691577720308242032279888024250179409222261839",
          "c": "54687071895183924055442269144489786903186459631877792294627879136747836413523"
        },
        "rev_reg": null,
        "witness": null
      },
      "credential": {
        "referent": "64ea2e85-c70f-45ad-b609-68bc1ac89816",
        "attrs": {
          "name": "Alice Jones"
        },
        "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
        "rev_reg_id": null,
        "cred_rev_id": null
      },
      "state": "stored",
      "updated_at": "2019-09-09 21:00:10.688590Z",
      "connection_id": "2d67c0a7-3c07-426c-b28f-89fec182f308",
      "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
      "credential_request": {
        "prover_did": "USz54LX588nXZzvJZaaauo",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
        "blinded_ms": {
          "u": "99368895797536005994311578723189357674473888721194302817275899605659815579082776035889727937509149843902587581396694097380001137952451816178530770768521813901129081437176205941944065200271520024859963251064451377398768846912432396109867523131209543363488226760277539406928453777223625182259241308969628882540671093876658006934832956644288049409819530272004889072620189012294592330334635260630961922620635703716969003181853188178982291121888203909561688206211503826185916253632379861409156552241548354871543971458468129569412836309227637169916178695946550538097767138914450365505044802717690371144577045034596177069218",
          "ur": null,
          "hidden_attributes": [
            "master_secret"
          ],
          "committed_attributes": {}
        },
        "blinded_ms_correctness_proof": {
          "c": "82814368957593600542678573704265961728440515441532250993783760615697056042766",
          "v_dash_cap": "2118452362398745861280226057596824191481494477242721958942324742953084725675464959425613275439996307006090128873526174900550688825200704332952595267412793247827461612669522329485045242589005220163235341676269260760388476609945675148280360463542384583398853903862359134202158782311554154739994184363677101683603079599084416381670111627232980638055599465177598913645868266764089443449862992176864925745186449013730471429866771461184116930725948848731317657299234761870227355190066369188033430582072763347201781851825566140580053014392699389990683680999169805660350968648440532935808946668533750546941833754340355282870786638599282983773855233579000116239048351315802722580655134903452234145646701421420006720424362392380",
          "m_caps": {
            "master_secret": "24225459579209831479420816101972689886146719984334583846534574626255831902742393762937117009729103049145090884891989587187027426846285733606614192343459832623110571090085221331919"
          },
          "r_caps": {}
        },
        "nonce": "1019073401153768641589280"
      },
      "thread_id": "db475c51-0630-4fbd-9ddb-28c7676f1fad",
      "auto_issue": false,
      "credential_id": "64ea2e85-c70f-45ad-b609-68bc1ac89816"
    }
  ]
}```


Alice

```GET /credentials/{id}  Fetch a credential from wallet by id```

Use the credential_id from the exchange record

"credential_id": "64ea2e85-c70f-45ad-b609-68bc1ac89816"


Response:

```json
{
  "referent": "64ea2e85-c70f-45ad-b609-68bc1ac89816",
  "attrs": {
    "name": "Alice Jones"
  },
  "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
  "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
  "rev_reg_id": null,
  "cred_rev_id": null
}```

Filed issues. Bad user experience to not report credential_id in GET credentials.

https://github.com/hyperledger/aries-cloudagent-python/issues/163
https://github.com/hyperledger/aries-cloudagent-python/issues/174


## 12) Request Proof of Credential by Faber of Alice


Faber request presentation (proof) of credential from Alice
Alice presents (proof) of credential to Faber
Normally this is just for reliability for Faber to make sure Alice has the credential and is
able to use it. Later Alice will need to respond to request of proof by some other Verifier Agent
not Faber.

Alice now has her Faber credential. Let’s have the Faber agent send a request
for a presentation (a proof) using that credential.
This should be pretty easy for you at this point.

From the Faber browser tab, get ready to execute the
 endpoint. Replace the pre-populated text with the following.
 In doing so, use the techniques we used in issuing the credential
 to replace the string values for each instance of cred_def_id (there are three)
 and connection_id.


The example in the tutorial was confusing because it did not include the value
field in the attributes. The attribute value field is documented here

https://github.com/hyperledger/aries-rfcs/tree/master/features/0037-present-proof

Also the Swagger documentation does not include the "value" field in its example.
So need to file issue.


Faber

```POST /presentation_exchange/send_request Creates and sends a presentation request```

Work but not asking for anything other than has name field in credential

```json
{
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "version": "1.0.0",
  "name": "Proof of Name",
  "requested_attributes":
  [
    {
      "name": "name",
      "restrictions":
      [
        {
          "cred_def_id" : "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
        }
      ]
    }
  ],
  "requested_predicates":
  [

  ]
}

```

"presentation_exchange_id": "f01e00a4-3fb9-468c-be05-1db65ac4075d",


```GET /presentation_exchange/{id}   Fetch a single presentation exchange record```


{
  "state": "verified",
  "presentation_exchange_id": "f01e00a4-3fb9-468c-be05-1db65ac4075d",


Not Work

```json
{
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "version": "1.0.0",
  "name": "Proof of Name",
  "requested_attributes":
  [
    {
      "name": "name",
      "restrictions":
      [
        {
          "cred_def_id" : "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
          "value": "Alice Jones"
        }
      ]
    }
  ],
  "requested_predicates":
  [

  ]
}

```
"presentation_exchange_id": "9c244b51-54c8-43f5-80ea-608b20f18702",


2019-09-09 16:08:43,889 aries_cloudagent.messaging.base_handler
WARNING Could not automatically construct presentation for presentation request
Proof of Name:1.0.0 because referent 568f5d0c-fba2-49b1-a28f-bdeb8a585349
did not produce exactly one credential result.
0 credentials were returned from the wallet.



Works

```json
{
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "version": "1.0.0",
  "name": "Proof of Name",
  "requested_attributes":
  [
    {
      "name": "name",
      "value": "Alice Jones",
      "restrictions":
      [
        {
          "cred_def_id" : "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
        }
      ]
    }
  ],
  "requested_predicates":
  [

  ]
}

```

"presentation_exchange_id": "e19e58a5-2aaf-41ba-a2d0-5a7d4e90ad28"

{
  "state": "verified",
  "presentation_exchange_id": "e19e58a5-2aaf-41ba-a2d0-5a7d4e90ad28",



Works

```json
{
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "version": "1.0.0",
  "name": "Proof of Name",
  "requested_attributes":
  [
    {
      "name": "name",
      "restrictions":
      [
        {
          "cred_def_id" : "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
        },
        {
          "value": "Alice Jones"
        }
      ]
    }
  ],
  "requested_predicates":
  [

  ]
}

```


Response:

```json
{
  "state": "request_sent",
  "presentation_exchange_id": "b3855d3c-bb35-4d6d-8a4d-a8b8952ed0e3",
  "initiator": "self",
  "created_at": "2019-09-09 22:12:08.050849Z",
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "updated_at": "2019-09-09 22:12:08.050849Z",
  "thread_id": "68670eed-005f-4e64-8e66-5950e03a8b1b",
  "presentation_request": {
    "name": "Proof of Name",
    "version": "1.0.0",
    "nonce": "239341901919028011378945058457791545863",
    "requested_attributes": {
      "a88aff02-454b-4256-b3de-09edde2620fb": {
        "name": "name",
        "restrictions": [
          {
            "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
          },
          {
            "value": "Alice Jones"
          }
        ]
      }
    },
    "requested_predicates": {}
  }
}

```

Faber Webhook Events:

```
Sink: /topic/presentations/ POST
JSON:
```

```json



```


Need presentation exchange ID from above record to verify

```
"presentation_exchange_id": "b3855d3c-bb35-4d6d-8a4d-a8b8952ed0e3"
```



```json
{
  "state": "verified",
  "presentation_exchange_id": "b3855d3c-bb35-4d6d-8a4d-a8b8952ed0e3",

   ...
```



## 13) Verify Presentation Request by Faber of Alice


Note that in the response, the state is request_sent.
That is because when the HTTP response was generated
(immediately after sending the request), Alice’s agent had not yet responded
to the request.

We’ll have to do another request to verify the presentation worked.
Copy the value of the presentation_exchange_id field from the response and
use it in executing the GET /presentation_exchange/{id} endpoint.
That should return a result showing a status of verified. Proof positive!



Faber

```GET /presentation_exchange/{id}   Fetch a single presentation exchange record```


```2d82d421-352d-40e6-96e5-85c34ae1533d```


Response:

```json
{
  "state": "verified",
  "presentation_exchange_id": "b3855d3c-bb35-4d6d-8a4d-a8b8952ed0e3",
  "initiator": "self",
  "created_at": "2019-09-09 22:12:08.050849Z",
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "verified": "true",
  "presentation": {
    "proof": {
      "proofs": [
        {
          "primary_proof": {
            "eq_proof": {
              "revealed_attrs": {
                "name": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
              },
              "a_prime": "19311514062893554794156386360318593598965491834528865020595158907394230030622126390958906042768081691066059045031228912675685230981054723222539663052029631072287093248064701781291932727184013012692978137971347533675538654191392771844737890541698885079117064568024439471403038774468759748598147211940229614691248012473419032653677768212396309915180718430728581361137012968447998697388450326245595982378020487842955393736129345645589539705489425814493282716642971000629891007116593965235054771298933501711095735051996240071410139626939936685452944608835264513033639613522551784950520034715192789610078722496660540814182",
              "e": "171405270980059950508790908636026825667200874421129347627673986940233538960414890172705219570252073603921730301531903359921996606983987974",
              "v": "1244797797155383752298176949059230595288155398541311391756734606603015227895904473006024841560778284339840525687724164558178786530646535612466700177206419426115303698538347134380134797484502165140101027901906794740691544113894878657770135176027511941621782004282123125680477754836747339734719901950273480385675704413167227658891842994074038496672038702679131542639828587384780566188720628385496382943852512386151867550283358450419156484731705734350532785859894483366860532872503998019476740900356253944742815701194290973249407793820474443879771424332213952560026111526831781708515506975861924647064214867665095411125046271037741501999687980069136403492036952954779647704648671104467445658557490050345271135999927250129958942957990414835030374900311438535191097871004663188298468042609268994753322715108086390021499177606729431957702435596698675987974219093375801721107266967801740552690090438525590877096140738769351534093",
              "m": {
                "master_secret": "8545735447283445461805531969117713876272332081151245409640390063906272831475114763983637742860841535202070152396533047028184753512260004505571579631071485215664756714092949878016"
              },
              "m2": "1087361321934536772812521556663840621473455965898024701742477021168896900965196715611804828591007705887268572881096020050165580793179178598878573142951303308713335744610599167127"
            },
            "ge_proofs": []
          },
          "non_revoc_proof": null
        }
      ],
      "aggregated_proof": {
        "c_hash": "66546425833986113448277623151434968071013873291483638187594202585119053496090",
        "c_list": [
          [
            152,
            250,
            6,
            73,
            225,
            31,
            27,
            152,
            105,
            74,
            203,
            88,
            201,
            135,
            198,
            1,
            29,
            177,
            243,
            20,
            116,
            138,
            103,
            41,
            185,
            199,
            168,
            235,
            95,
            133,
            181,
            2,
            227,
            94,
            156,
            46,
            127,
            124,
            230,
            86,
            12,
            39,
            142,
            29,
            148,
            247,
            97,
            201,
            120,
            2,
            53,
            194,
            33,
            109,
            0,
            98,
            197,
            245,
            100,
            235,
            38,
            237,
            58,
            107,
            192,
            202,
            244,
            124,
            7,
            156,
            45,
            196,
            144,
            118,
            172,
            7,
            243,
            227,
            2,
            111,
            147,
            94,
            156,
            163,
            166,
            98,
            94,
            1,
            11,
            235,
            102,
            81,
            59,
            135,
            207,
            19,
            116,
            11,
            74,
            207,
            219,
            82,
            79,
            32,
            244,
            202,
            96,
            159,
            21,
            25,
            143,
            155,
            45,
            128,
            203,
            86,
            3,
            38,
            168,
            212,
            180,
            142,
            91,
            29,
            187,
            93,
            34,
            253,
            121,
            178,
            26,
            132,
            176,
            115,
            134,
            16,
            8,
            90,
            41,
            5,
            204,
            121,
            194,
            151,
            14,
            25,
            225,
            0,
            186,
            177,
            106,
            180,
            88,
            76,
            196,
            68,
            15,
            250,
            229,
            9,
            164,
            29,
            63,
            89,
            225,
            43,
            223,
            227,
            115,
            108,
            25,
            36,
            138,
            116,
            186,
            190,
            10,
            178,
            139,
            200,
            216,
            89,
            7,
            241,
            152,
            46,
            198,
            252,
            127,
            64,
            216,
            40,
            164,
            160,
            67,
            77,
            26,
            253,
            111,
            137,
            254,
            71,
            210,
            140,
            50,
            21,
            161,
            25,
            57,
            184,
            101,
            194,
            152,
            242,
            225,
            192,
            129,
            36,
            245,
            113,
            240,
            233,
            8,
            182,
            147,
            191,
            52,
            121,
            43,
            5,
            185,
            8,
            126,
            151,
            123,
            102,
            246,
            250,
            196,
            44,
            172,
            218,
            243,
            193,
            48,
            90,
            162,
            174,
            223,
            91,
            161,
            63,
            241,
            168,
            243,
            102
          ]
        ]
      }
    },
    "requested_proof": {
      "revealed_attrs": {
        "a88aff02-454b-4256-b3de-09edde2620fb": {
          "sub_proof_index": 0,
          "raw": "Alice Jones",
          "encoded": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
        }
      },
      "self_attested_attrs": {},
      "unrevealed_attrs": {},
      "predicates": {}
    },
    "identifiers": [
      {
        "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
        "rev_reg_id": null,
        "timestamp": null
      }
    ]
  },
  "updated_at": "2019-09-09 22:12:08.347524Z",
  "thread_id": "68670eed-005f-4e64-8e66-5950e03a8b1b",
  "presentation_request": {
    "name": "Proof of Name",
    "version": "1.0.0",
    "nonce": "239341901919028011378945058457791545863",
    "requested_attributes": {
      "a88aff02-454b-4256-b3de-09edde2620fb": {
        "name": "name",
        "restrictions": [
          {
            "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
          },
          {
            "value": "Alice Jones"
          }
        ]
      }
    },
    "requested_predicates": {}
  }
}

```

Faber Webhook Events:

## 14 Verify Presentation Exchange at Alice

We can also see that the presentation at Alice

Alice

```GET /presentation_exchange Fetch all presentation exchange records```


Presentation Exchange Id:

"presentation_exchange_id": "0362037e-3a72-4691-a5de-157c9fa7443e",


```GET /presentation_exchange/{id}   ```

Response:

```json
{
  "created_at": "2019-09-09 22:12:08.099329Z",
  "presentation_exchange_id": "0362037e-3a72-4691-a5de-157c9fa7443e",
  "presentation_request": {
    "name": "Proof of Name",
    "version": "1.0.0",
    "nonce": "239341901919028011378945058457791545863",
    "requested_attributes": {
      "a88aff02-454b-4256-b3de-09edde2620fb": {
        "name": "name",
        "restrictions": [
          {
            "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
          },
          {
            "value": "Alice Jones"
          }
        ]
      }
    },
    "requested_predicates": {}
  },
  "initiator": "external",
  "connection_id": "2d67c0a7-3c07-426c-b28f-89fec182f308",
  "state": "presentation_sent",
  "updated_at": "2019-09-09 22:12:08.196578Z",
  "presentation": {
    "proof": {
      "proofs": [
        {
          "primary_proof": {
            "eq_proof": {
              "revealed_attrs": {
                "name": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
              },
              "a_prime": "19311514062893554794156386360318593598965491834528865020595158907394230030622126390958906042768081691066059045031228912675685230981054723222539663052029631072287093248064701781291932727184013012692978137971347533675538654191392771844737890541698885079117064568024439471403038774468759748598147211940229614691248012473419032653677768212396309915180718430728581361137012968447998697388450326245595982378020487842955393736129345645589539705489425814493282716642971000629891007116593965235054771298933501711095735051996240071410139626939936685452944608835264513033639613522551784950520034715192789610078722496660540814182",
              "e": "171405270980059950508790908636026825667200874421129347627673986940233538960414890172705219570252073603921730301531903359921996606983987974",
              "v": "1244797797155383752298176949059230595288155398541311391756734606603015227895904473006024841560778284339840525687724164558178786530646535612466700177206419426115303698538347134380134797484502165140101027901906794740691544113894878657770135176027511941621782004282123125680477754836747339734719901950273480385675704413167227658891842994074038496672038702679131542639828587384780566188720628385496382943852512386151867550283358450419156484731705734350532785859894483366860532872503998019476740900356253944742815701194290973249407793820474443879771424332213952560026111526831781708515506975861924647064214867665095411125046271037741501999687980069136403492036952954779647704648671104467445658557490050345271135999927250129958942957990414835030374900311438535191097871004663188298468042609268994753322715108086390021499177606729431957702435596698675987974219093375801721107266967801740552690090438525590877096140738769351534093",
              "m": {
                "master_secret": "8545735447283445461805531969117713876272332081151245409640390063906272831475114763983637742860841535202070152396533047028184753512260004505571579631071485215664756714092949878016"
              },
              "m2": "1087361321934536772812521556663840621473455965898024701742477021168896900965196715611804828591007705887268572881096020050165580793179178598878573142951303308713335744610599167127"
            },
            "ge_proofs": []
          },
          "non_revoc_proof": null
        }
      ],
      "aggregated_proof": {
        "c_hash": "66546425833986113448277623151434968071013873291483638187594202585119053496090",
        "c_list": [
          [
            152,
            250,
            6,
            73,
            225,
            31,
            27,
            152,
            105,
            74,
            203,
            88,
            201,
            135,
            198,
            1,
            29,
            177,
            243,
            20,
            116,
            138,
            103,
            41,
            185,
            199,
            168,
            235,
            95,
            133,
            181,
            2,
            227,
            94,
            156,
            46,
            127,
            124,
            230,
            86,
            12,
            39,
            142,
            29,
            148,
            247,
            97,
            201,
            120,
            2,
            53,
            194,
            33,
            109,
            0,
            98,
            197,
            245,
            100,
            235,
            38,
            237,
            58,
            107,
            192,
            202,
            244,
            124,
            7,
            156,
            45,
            196,
            144,
            118,
            172,
            7,
            243,
            227,
            2,
            111,
            147,
            94,
            156,
            163,
            166,
            98,
            94,
            1,
            11,
            235,
            102,
            81,
            59,
            135,
            207,
            19,
            116,
            11,
            74,
            207,
            219,
            82,
            79,
            32,
            244,
            202,
            96,
            159,
            21,
            25,
            143,
            155,
            45,
            128,
            203,
            86,
            3,
            38,
            168,
            212,
            180,
            142,
            91,
            29,
            187,
            93,
            34,
            253,
            121,
            178,
            26,
            132,
            176,
            115,
            134,
            16,
            8,
            90,
            41,
            5,
            204,
            121,
            194,
            151,
            14,
            25,
            225,
            0,
            186,
            177,
            106,
            180,
            88,
            76,
            196,
            68,
            15,
            250,
            229,
            9,
            164,
            29,
            63,
            89,
            225,
            43,
            223,
            227,
            115,
            108,
            25,
            36,
            138,
            116,
            186,
            190,
            10,
            178,
            139,
            200,
            216,
            89,
            7,
            241,
            152,
            46,
            198,
            252,
            127,
            64,
            216,
            40,
            164,
            160,
            67,
            77,
            26,
            253,
            111,
            137,
            254,
            71,
            210,
            140,
            50,
            21,
            161,
            25,
            57,
            184,
            101,
            194,
            152,
            242,
            225,
            192,
            129,
            36,
            245,
            113,
            240,
            233,
            8,
            182,
            147,
            191,
            52,
            121,
            43,
            5,
            185,
            8,
            126,
            151,
            123,
            102,
            246,
            250,
            196,
            44,
            172,
            218,
            243,
            193,
            48,
            90,
            162,
            174,
            223,
            91,
            161,
            63,
            241,
            168,
            243,
            102
          ]
        ]
      }
    },
    "requested_proof": {
      "revealed_attrs": {
        "a88aff02-454b-4256-b3de-09edde2620fb": {
          "sub_proof_index": 0,
          "raw": "Alice Jones",
          "encoded": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
        }
      },
      "self_attested_attrs": {},
      "unrevealed_attrs": {},
      "predicates": {}
    },
    "identifiers": [
      {
        "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
        "rev_reg_id": null,
        "timestamp": null
      }
    ]
  },
  "thread_id": "68670eed-005f-4e64-8e66-5950e03a8b1b"
}

```



## 12, 13, 14 Alternate


Change format of request. To simpler format not sure why it works

Faber

```POST /presentation_exchange/send_request Creates and sends a presentation request```


```json
{
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "version": "1.0.0",
  "name": "Proof of Name",
  "requested_attributes":
  [
    {
      "name": "name",
      "value": "Alice Jones",
      "cred_def_id" : "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
    }
  ],
  "requested_predicates":
  [

  ]
}

```


Response:

```json
{
  "state": "request_sent",
  "presentation_exchange_id": "e391a2fd-ff3d-4ead-b74b-b00224d6b805",
  "initiator": "self",
  "created_at": "2019-09-09 22:20:11.032265Z",
  "connection_id": "d965bd54-affb-4e11-ba8e-ea54a3214123",
  "updated_at": "2019-09-09 22:20:11.032265Z",
  "thread_id": "27cb1e9d-9dca-41a6-86b2-9b6cc7064e00",
  "presentation_request": {
    "name": "Proof of Name",
    "version": "1.0.0",
    "nonce": "119525911828023084516916940999947747843",
    "requested_attributes": {
      "55cce48e-c037-4e11-8f97-8988056d57c1": {
        "name": "name",
        "value": "Alice Jones",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
      }
    },
    "requested_predicates": {}
  }
}

```

"presentation_exchange_id": "e391a2fd-ff3d-4ead-b74b-b00224d6b805"

Faber

```GET /presentation_exchange/{id}   Fetch a single presentation exchange record```


```e391a2fd-ff3d-4ead-b74b-b00224d6b805```

```json
{
  "state": "verified",
  "presentation_exchange_id": "e391a2fd-ff3d-4ead-b74b-b00224d6b805",

```


We can also see that the presentation at Alice

Alice

```GET /presentation_exchange Fetch all presentation exchange records```


Presentation Exchange Id:

"presentation_exchange_id": "a8cf1a5f-84a4-4401-8f5c-6f03424bff99",


```GET /presentation_exchange/{id}   ```

a8cf1a5f-84a4-4401-8f5c-6f03424bff99





Response:

```json
{
  "created_at": "2019-09-09 22:20:11.084361Z",
  "presentation_exchange_id": "a8cf1a5f-84a4-4401-8f5c-6f03424bff99",
  "presentation_request": {
    "name": "Proof of Name",
    "version": "1.0.0",
    "nonce": "119525911828023084516916940999947747843",
    "requested_attributes": {
      "55cce48e-c037-4e11-8f97-8988056d57c1": {
        "name": "name",
        "value": "Alice Jones",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default"
      }
    },
    "requested_predicates": {}
  },
  "initiator": "external",
  "connection_id": "2d67c0a7-3c07-426c-b28f-89fec182f308",
  "state": "presentation_sent",
  "updated_at": "2019-09-09 22:20:12.045819Z",
  "presentation": {
    "proof": {
      "proofs": [
        {
          "primary_proof": {
            "eq_proof": {
              "revealed_attrs": {
                "name": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
              },
              "a_prime": "65193207043853525141306632816154501471693381325711630491729111589216831720889446458220618354745456717668674006552203689480109056493235314613729478322677778722952396619459189099503201631522144420987762406709739036494894080090741911691668314358112735516966308194512262642557989659378365189794412558482243908293632610198976528884655638889371404564461719540350885365202310938129902946197086284879509799450794958735950023880645101870877606499304433727562590118863003717012478137928775230373191046942224326627706470196690638162464454019360874195476568032109978609122580650073057890209119723963310441273057560658420018514401",
              "e": "155743265709338075531532260329591309859444392459483149932977474057699006153473776819518850450375654416250336684384788259608969628207239714",
              "v": "835821314558612303282950692816333846561090395710032444239673069137754844501715842845969173466478404170182502561046107445379177548050247996745635193826081826031675531373176883635697160721284333322532124876180758634580140743073615444688204567312349212336208614480981407125804538016754837199617385950252726243321830096083914143929973130400202198361632174033642134738762659080776969190457149625028037903880484521072474189015796501199038737366304867478542312786475862477586966034381206035250525119138483923216664708728874636549065178915680454483801452295246208639023316887062959897793613921511071246471084528498648329951481765612031011349600288356245053758519194494056232483469210535792668304015348189857887797065189043955538994084784353356660607177277074967005304545480831756988867027756215291985349546760321623245132836489120452118297364480684320943952962911957981919277435685460061706375687624414661622611486516468103354596",
              "m": {
                "master_secret": "900270590529555049202916920394037062168517532030457230411319331732005716955337118949903201648849120740460632480854392659947034860615387532717575631929590231116440164086449280877"
              },
              "m2": "6485678138771203250220466104535891509576077638262666227158060832247270943638118112834295551811488380199101653507406440673015969950899002100911469259237596865466878411063081540045"
            },
            "ge_proofs": []
          },
          "non_revoc_proof": null
        }
      ],
      "aggregated_proof": {
        "c_hash": "2688947127175083474224811548683598800592660163118506231929327072862926439292",
        "c_list": [
          [
            2,
            4,
            109,
            255,
            77,
            223,
            116,
            211,
            211,
            131,
            38,
            245,
            177,
            184,
            139,
            255,
            69,
            137,
            203,
            33,
            113,
            57,
            220,
            127,
            242,
            91,
            41,
            130,
            193,
            88,
            228,
            180,
            0,
            117,
            83,
            62,
            238,
            225,
            140,
            94,
            6,
            223,
            11,
            11,
            89,
            205,
            215,
            52,
            236,
            32,
            238,
            203,
            9,
            83,
            245,
            28,
            89,
            174,
            211,
            56,
            145,
            204,
            247,
            188,
            22,
            62,
            67,
            185,
            87,
            4,
            254,
            148,
            157,
            122,
            136,
            80,
            45,
            186,
            180,
            142,
            208,
            126,
            30,
            126,
            173,
            137,
            11,
            137,
            35,
            132,
            101,
            98,
            55,
            82,
            157,
            61,
            34,
            142,
            157,
            145,
            22,
            149,
            14,
            116,
            73,
            103,
            8,
            99,
            220,
            217,
            193,
            115,
            101,
            1,
            7,
            67,
            0,
            180,
            76,
            15,
            195,
            73,
            112,
            29,
            138,
            210,
            209,
            34,
            40,
            61,
            22,
            174,
            219,
            40,
            222,
            146,
            54,
            248,
            94,
            115,
            230,
            227,
            159,
            68,
            94,
            51,
            90,
            238,
            246,
            159,
            118,
            252,
            174,
            223,
            128,
            206,
            205,
            30,
            42,
            106,
            198,
            147,
            57,
            82,
            97,
            101,
            71,
            187,
            83,
            45,
            216,
            171,
            241,
            219,
            245,
            90,
            34,
            252,
            157,
            157,
            141,
            57,
            227,
            203,
            65,
            9,
            93,
            32,
            197,
            174,
            248,
            68,
            197,
            150,
            115,
            32,
            246,
            209,
            110,
            199,
            168,
            18,
            190,
            255,
            213,
            2,
            68,
            50,
            214,
            156,
            104,
            222,
            102,
            146,
            104,
            12,
            92,
            21,
            5,
            89,
            77,
            150,
            206,
            62,
            31,
            38,
            194,
            224,
            245,
            21,
            175,
            150,
            21,
            114,
            170,
            107,
            146,
            86,
            243,
            88,
            48,
            24,
            132,
            125,
            210,
            107,
            219,
            151,
            126,
            42,
            64,
            21,
            87,
            132,
            109,
            9,
            225
          ]
        ]
      }
    },
    "requested_proof": {
      "revealed_attrs": {
        "55cce48e-c037-4e11-8f97-8988056d57c1": {
          "sub_proof_index": 0,
          "raw": "Alice Jones",
          "encoded": "72896232743708443677449555551687504476536417389324439453514323796296385992918"
        }
      },
      "self_attested_attrs": {},
      "unrevealed_attrs": {},
      "predicates": {}
    },
    "identifiers": [
      {
        "schema_id": "3avoBCqDMFHFaKUHug9s8W:2:fabername:0.1.0",
        "cred_def_id": "3avoBCqDMFHFaKUHug9s8W:3:CL:13:default",
        "rev_reg_id": null,
        "timestamp": null
      }
    ]
  },
  "thread_id": "27cb1e9d-9dca-41a6-86b2-9b6cc7064e00"
}


```




### Notes

As with the issue credential process, the agents handled some of the
presentation steps without bothering the controller.
In this case, Alice’s agent processed the presentation request automatically
because it was started with the --auto-respond-presentation-request parameter set,
and her wallet contained exactly one credential that satisfied the
presentation-request from the Faber agent. Similarly, the Faber agent was
started with the --auto-verify-presentation parameter and so on receipt of
the presentation, it verified the presentation and updated the status accordingly.



## Conclusion


That’s the OpenAPI-based tutorial. Feel free to play with the API and learn
how it works. More importantly, as you implement a controller, use the OpenAPI
user interface to test out the calls you will be using as you go.
The list of API calls is grouped by protocol and if you are familiar with
the protocols (Aries RFCs) the API call names should be pretty obvious.

