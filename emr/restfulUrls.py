__author__ = 'JWang'
from rest_framework import routers
from emr.restfulAPI import *

router = routers.DefaultRouter()

router.register(r'scContent', scContentViewSet,base_name='scContent')
router.register(r'scComment', scCommentViewSet,base_name='scComment')
router.register(r'scMessage', scMessageViewSet,base_name='scMessage')

router.register(r'users', UserViewSet,base_name='users')
router.register(r'usersEx', UserExtInfoViewSet,base_name='usersEx')
router.register(r'selfUsersEx', selfUserExtInfoViewSet,base_name='selfUsersEx')
router.register(r'selfRelatedUsersEx', selfRelatedUserExtInfoViewSet,base_name='selfRelatedUsersEx')
router.register(r'chatrecord', ChatRecordViewSet,base_name='chatrecord')
router.register(r'bodyTemperature', bodyTemperatureViewSet,base_name='bodyTemperature')
router.register(r'bloodpressure', bloodpressureViewSet,base_name='bloodpressure')
router.register(r'bloodglucose', mdlbloodglucoseViewSet,base_name='bloodglucose')
router.register(r'medicineLib', mdlMedicineLibViewSet,base_name='medicineLib')
router.register(r'medicineNoteTask', mdlMedicineNoteTaskViewSet,base_name='medicineNoteTask')
router.register(r'medicineNoteCompletedRecord', mdlMedicineNoteCompletedRecordViewSet,base_name='medicineNoteCompletedRecord')
router.register(r'instrument', mdlInstrumentViewSet,base_name='instrument')
router.register(r'myMedicalOrgnization', mdlmyMedicalOrgnizationViewSet,base_name='myMedicalOrgnization')
router.register(r'myDoctorList', mdlmyDoctorListViewSet,base_name='myDoctorList')
router.register(r'myMedicineEatRecord', mdlmyMedicineEatRecordViewSet,base_name='myMedicineEatRecord')
router.register(r'myMedicalRecords', mdlmyMedicalRecordsViewSet,base_name='myMedicalRecords')
router.register(r'myFluorescenceData', mdlmyFluorescenceDataViewSet)
router.register(r'myFluorescenceInfo', mdlmyFluorescenceInfoViewSet)
router.register(r'myFluorescenceTestert', mdlmyFluorescenceTesterViewSet)
router.register(r'myTestCard', mdlmyTestCardViewSet)
router.register(r'myTestPeopleInfo', mdlmyTestPeopleInfoViewSet)
router.register(r'myReport', mdlmyReportViewSet)
router.register(r'myCardUseInfo', mdlmyCardUseInfoViewSet)
router.register(r'myStorageTable', mdlmyStorageTableViewSet)
