export default function createFormEntry(data, code) {
  return {
    id: code,
    createdAt: Date.now(),
    personInfo: {
      address: data.address,
      passport: data.passport,
      FamilyName: data.FamilyName,
      SureName: data.Surname,
      name: data.name,
      phoneNumber: data.phoneNumber,
    },
    receiverInfo: {
      address2: data.address2,
      passport2: data.passport2,
      receiverFamilyName: data.receiverFamilyName,
      receiverSureName: data.receiverSurename,
      receiverName: data.receiverName,
      receiverPhoneNumber: data.receiverPhoneNumber,
    }
  };
}
