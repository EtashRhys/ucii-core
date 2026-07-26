from ucii import Identity, IdentityType


identity = Identity(
    name="Example Human",
    identity_type=IdentityType.HUMAN,
)


print("UCII Core Identity Example")
print()
print("Identity created")
print()
print("Name:", identity.name)
print("Type:", identity.identity_type.value)
print("ID:", identity.id)
