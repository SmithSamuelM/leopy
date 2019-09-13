#  Notes from Indy-SDK Docs

https://github.com/hyperledger/indy-sdk/blob/master/docs/how-tos/negotiate-proof/


Example proof request


log("9. Prover gets Credentials for Proof Request")

```javascript
    const proofRequest = {
        'nonce': '123432421212',
        'name': 'proof_req_1',
        'version': '0.1',
        'requested_attributes': {
            'attr1_referent': {
                'name': 'name',
                'restrictions': [{
                    'cred_def_id': credDefId
                    /*
                    'issuer_did': issuerDid,
                    'schema_key': schemaKey
                    */
                }]
            }
        },
        'requested_predicates': {
            'predicate1_referent': {
                'name': 'age',
                'p_type': '>=',
                'p_value': 18,
                'restrictions': [{'issuer_did': issuerDid}]
            }
        }
    }
    
```    

https://github.com/hyperledger/indy-sdk/blob/master/docs/getting-started/indy-walkthrough.md

    
```python    
# Acme Agent
acme['job_application_proof_request'] = json.dumps({
  'nonce': '1432422343242122312411212',
  'name': 'Job-Application',
  'version': '0.1',
  'requested_attributes': {
      'attr1_referent': {
          'name': 'first_name'
      },
      'attr2_referent': {
          'name': 'last_name'
      },
      'attr3_referent': {
          'name': 'degree',
          'restrictions': [{'cred_def_id': faber['transcript_cred_def_id']}]
      },
      'attr4_referent': {
          'name': 'status',
          'restrictions': [{'cred_def_id': faber['transcript_cred_def_id']}]
      },
      'attr5_referent': {
          'name': 'ssn',
          'restrictions': [{'cred_def_id': faber['transcript_cred_def_id']}]
      },
      'attr6_referent': {
          'name': 'phone_number'
      }
  },
  'requested_predicates': {
      'predicate1_referent': {
          'name': 'average',
          'p_type': '>=',
          'p_value': 4,
          'restrictions': [{'cred_def_id': faber['transcript_cred_def_id']}]
      }
  }
})
  
```

Only restrictions are on predicates.  What does it mean to request attributes but not
restrict them?

"Notice that some attributes are verifiable and some are not.

The proof request says that SSN, degree, and graduation status in the Credential must be formally asserted by an issuer and schema_key. Notice also that the first_name, last_name and phone_number are not required to be verifiable. By not tagging these credentials with a verifiable status, Acme’s credential request is saying it will accept Alice’s own credential about her names and phone numbers."

What is not being answered is have value restriction works.

Looks like requested attributes just returns requested attributes. Only requested predicates
does anything



https://github.com/hyperledger/indy-sdk/tree/master/docs/design/002-anoncreds


Not very helpful

Looks like its high level, tutuorial, and then code
no intermediate level documentation that says heres how a proof works heres what the fields mean.

Just examples.

