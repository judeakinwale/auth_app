from company import models


def sample_phone(phone_number='010000001', **kwargs):
  """create and return a sample phone number"""
  defaults = {}.update(kwargs)
  return models.Phone.objects.create(phone_number=phone_number, **defaults)



def sample_company(name: str = "Company 1", email: str = "company1@app.com", **kwargs):
  """create and return sample company"""
  defaults = {
    'name': name,
    'email': email,
  }
  defaults.update(kwargs)
  return models.Company.objects.create(**defaults)


def test_all_model_attributes(insance, payload, model, serializer):
  """test model attributes against a payload, with instance being self in a testcase class """
  ignored_keys = ['image', 'logo']
  relevant_keys = sorted(set(payload.keys()).difference(ignored_keys))
  for key in relevant_keys:
    try:
      insance.assertEqual(payload[key], getattr(model, key))
    except Exception:
      insance.assertEqual(payload[key], serializer.data[key])
