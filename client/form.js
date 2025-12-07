export default function createFormEntry(data, code) {
  return {
    id: code,
    createdAt: Date.now(),
    personInfo: {
      address: data.personInfo.address,
      passport: data.personInfo.passport,
      FamilyName: data.personInfo.FamilyName,
      SureName: data.personInfo.SureName,
      name: data.personInfo.name,
      phoneNumber: data.personInfo.phoneNumber,
    },
    receiverInfo: {
      address2: data.receiverInfo.address2,
      passport2: data.receiverInfo.passport2,
      receiverFamilyName: data.receiverInfo.receiverFamilyName,
      receiverSureName: data.receiverInfo.receiverSureName,
      receiverName: data.receiverInfo.receiverName,
      receiverPhoneNumber: data.receiverInfo.receiverPhoneNumber,
    }
  };
}
