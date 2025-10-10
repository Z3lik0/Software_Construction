import func

def test_add_happy():
  expected_value = 5
  actual_value = func.add(3,2)
  assert actual_value == expected_value

def test_add_wrong():
  assert func.add(4,4) == 8

print(globals())