__author__ = 'JWang'

from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import FormParser, FileUploadParser,MultiPartParser
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status
from emr import models
from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

class mdlSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    # filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username',)
    # def get_queryset(self):
    #     query=[]
    #     try:
    #         user = self.request.user
    #         query.append(user)
    #     except:
    #         query = None
    #     return query
#######################################################################################
class UserExtRelativeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlUserExtInfo
        fields = ("user","uniqEmail","uniqMobilePhone","nickname","demo","user_type","user_image","workday", "name","QR")

class UserExtInfoSerializer(serializers.ModelSerializer):
    relative_set = UserExtRelativeInfoSerializer(source="relative_user",many=True,read_only=True)
    class Meta:
        model = models.mdlUserExtInfo
        fields = ("user","email_activation_key","uniqEmail", "is_uniqEmailActivated","uniqMobilePhone","is_uniqMobilePhoneActivated",
            "sex","educationbackground","datebirth","nickname","addressline1","addressline2","state","city","district","zipcode",
            "is_locked","demo","user_type","user_image","name","home","height","weight","blood_type","subject","company","jobNumber","achivement",
            "personID","Vocational_qualification_certificate","VQCID","publicGender","publicHome","QR","roamingtime","workday","relative_set")

    # class Meta:
    #     model = models.mdlUserExtInfo
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlUserExtInfo.objects.create(**validated_data)
# ViewSets define the view behavior.
class UserExtInfoViewSet(viewsets.ModelViewSet):
    queryset = models.mdlUserExtInfo.objects.all()
    serializer_class = UserExtInfoSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('nickname','user_type')
    # def get_queryset(self):
    #     query=[]
    #     try:
    #         user = self.request.user
    #         query.append(user.mdluserextinfo)
    #     except:
    #         query = None
    #     return query
class selfUserExtInfoViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlUserExtInfo.objects.all()
    serializer_class = UserExtInfoSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser, )
    #filter_fields = ('nickname','user_type')
    def get_queryset(self):
        query=[]
        try:
            user = self.request.user
            query.append(user.mdluserextinfo)
        except:
            query = None
        return query

class selfRelatedUserExtInfoViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlUserExtInfo.objects.all()
    serializer_class = UserExtInfoSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser, )
    #filter_fields = ('nickname','user_type')
    def get_queryset(self):
        query=[]
        try:
            user = self.request.user
            relative_users = user.mdluserextinfo.relative_user.all()
            query = relative_users
        except:
            query = None
        return query
# Routers provide an easy way of automatically determining the URL conf.

#######################################################################################
class ChatRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlChatRecord
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlChatRecord.objects.create(**validated_data)

# ViewSets define the view behavior.
class ChatRecordViewSet(viewsets.ModelViewSet):
    queryset = models.mdlChatRecord.objects.all()
    serializer_class = ChatRecordSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class bodyTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlbodyTemperature
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlbodyTemperature.objects.create(**validated_data)
# ViewSets define the view behavior.
class bodyTemperatureViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlbodyTemperature.objects.all()
    serializer_class = bodyTemperatureSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    #filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('temperature',)
    def get_queryset(self):
        try:
            user = self.request.user
            query = user.mdluserextinfo.mdlbodytemperature_set.all()
        except:
            query = None#models.mdlbodyTemperature.objects.all()
        return query
#######################################################################################
class bloodpressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlbloodpressure
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlbloodpressure.objects.create(**validated_data)
# ViewSets define the view behavior.
class bloodpressureViewSet(viewsets.ModelViewSet):
    queryset = models.mdlbloodpressure.objects.all()
    serializer_class = bloodpressureSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('user',)
    pagination_class = mdlSetPagination
    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         query = user.mdluserextinfo.mdlbloodpressure_set.all()
    #     except:
    #         query = None
    #     return query
 #######################################################################################
class mdlbloodglucoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlbloodglucose
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlbloodglucose.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlbloodglucoseViewSet(viewsets.ModelViewSet):
    queryset = models.mdlbloodglucose.objects.all()
    serializer_class = mdlbloodglucoseSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('user',)
    pagination_class = mdlSetPagination
    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         query = user.mdluserextinfo.mdlbloodglucose_set.all()
    #     except:
    #         query = None
    #     return query
#######################################################################################
class mdlMedicineLibSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlMedicineLib
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlMedicineLib.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlMedicineLibViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlMedicineLib.objects.all()
    serializer_class = mdlMedicineLibSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

    def get_queryset(self):
        try:
            user = self.request.user
            query = user.mdluserextinfo.mdlmedicinelib_set.all()
        except:
            query = None
        return query
#######################################################################################
class mdlMedicineNoteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlMedicineNoteTask
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlMedicineNoteTask.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlMedicineNoteTaskViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlMedicineNoteTask.objects.all()
    serializer_class = mdlMedicineNoteTaskSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

    def get_queryset(self):
        try:
            user = self.request.user
            query = user.mdluserextinfo.mdlmedicinenotetask_set.all()
        except:
            query = None
        return query

#######################################################################################
class mdlMedicineNoteCompletedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlMedicineNoteCompletedRecord
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlMedicineNoteCompletedRecord.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlMedicineNoteCompletedRecordViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlMedicineNoteCompletedRecord.objects.all()
    serializer_class = mdlMedicineNoteCompletedRecordSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

    def get_queryset(self):
        try:
            user = self.request.user
            query = user.mdluserextinfo.mdlmedicinenotecompletedrecord_set.all()
        except:
            query = None
        return query
#######################################################################################
class mdlInstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlInstrument
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlInstrument.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlInstrumentViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlInstrument.objects.all()
    serializer_class = mdlInstrumentSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

    def get_queryset(self):
        try:
            user = self.request.user
            query = user.mdluserextinfo.mdlinstrument_set.all()
        except:
            query = None
        return query

#######################################################################################
class mdlmyMedicalOrgnizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyMedicalOrgnization
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyMedicalOrgnization.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyMedicalOrgnizationViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlmyMedicalOrgnization.objects.all()
    serializer_class = mdlmyMedicalOrgnizationSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

    def get_queryset(self):
        try:
            user = self.request.user
            query = user.mdluserextinfo.mdlmymedicalorgnization_set.all()
        except:
            query = None
        return query
#######################################################################################
class mdlmyDoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyDoctorList
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyDoctorList.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyDoctorListViewSet(viewsets.ModelViewSet):
    #queryset = models.mdlmyDoctorList.objects.all()
    serializer_class = mdlmyDoctorListSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

    def get_queryset(self):
        try:
            user = self.request.user
            query = user.mdluserextinfo.mdlmydoctorlist_set.all()
        except:
            query = None
        return query
#######################################################################################
class mdlmyMedicineEatRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyMedicineEatRecord
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyMedicineEatRecord.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyMedicineEatRecordViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyMedicineEatRecord.objects.all()
    serializer_class = mdlmyMedicineEatRecordSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('user',)
    pagination_class = mdlSetPagination

    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         query = user.mdluserextinfo.mdlmymedicineeatrecord_set.all()
    #     except:
    #         query = None
    #     return query

#######################################################################################
class mdlmyMedicalRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyMedicalRecords
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyMedicalRecords.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyMedicalRecordsViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyMedicalRecords.objects.all()
    serializer_class = mdlmyMedicalRecordsSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('user','recordType')
    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         query = user.mdluserextinfo.mdlmymedicalrecords_set.all()
    #     except:
    #         query = None
    #     return query

#######################################################################################
class mdlmyFluorescenceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyFluorescenceData
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyFluorescenceData.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyFluorescenceDataViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyFluorescenceData.objects.all()
    serializer_class = mdlmyFluorescenceDataSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('DeviceID',)
    pagination_class = mdlSetPagination

#######################################################################################
class mdlmyFluorescenceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyFluorescenceInfo
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyFluorescenceInfo.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyFluorescenceInfoViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyFluorescenceInfo.objects.all()
    serializer_class = mdlmyFluorescenceInfoSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class mdlmyFluorescenceTesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyFluorescenceTester
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyFluorescenceTester.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyFluorescenceTesterViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyFluorescenceTester.objects.all()
    serializer_class = mdlmyFluorescenceTesterSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class mdlmyTestCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyTestCard
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyTestCard.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyTestCardViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyTestCard.objects.all()
    serializer_class = mdlmyTestCardSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class mdlmyTestPeopleInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyTestPeopleInfo
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyTestPeopleInfo.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyTestPeopleInfoViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyTestPeopleInfo.objects.all()
    serializer_class = mdlmyTestPeopleInfoSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class mdlmyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyReport
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyReport.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyReportViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyReport.objects.all()
    serializer_class = mdlmyReportSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class mdlmyCardUseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyCardUseInfo
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyCardUseInfo.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyCardUseInfoViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyCardUseInfo.objects.all()
    serializer_class = mdlmyCardUseInfoSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class mdlmyStorageTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.mdlmyStorageTable
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return models.mdlmyStorageTable.objects.create(**validated_data)
# ViewSets define the view behavior.
class mdlmyStorageTableViewSet(viewsets.ModelViewSet):
    queryset = models.mdlmyStorageTable.objects.all()
    serializer_class = mdlmyStorageTableSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser, )

#######################################################################################
class scCommentTracksSerializer(serializers.ModelSerializer):
    uid_name = serializers.ReadOnlyField(source='uid.nickname')
    uid_avator = serializers.ReadOnlyField(source='uid.user_image.url')
    # uid = serializers.RelatedField(source='uid', read_only=True)
    class Meta:
        model = models.scComment
        fields = ('pk','uid','wid','ctext','time','uid_name','uid_avator')
class scContentSerializer(serializers.ModelSerializer):
    uid_name = serializers.ReadOnlyField(source='uid.nickname')
    uid_avator = serializers.ReadOnlyField(source='uid.user_image.url')
    scComment_set = scCommentTracksSerializer(many=True,read_only=True)
    class Meta:
        model = models.scContent
        fields = ('pk','uid','text','img1', 'img2','img3','time','uid_name','uid_avator','scComment_set')
    def create(self, validated_data):
        return models.scContent.objects.create(**validated_data)
# ViewSets define the view behavior.
class scContentViewSet(viewsets.ModelViewSet):
    queryset = models.scContent.objects.all()
    serializer_class = scContentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('uid',)
    pagination_class = mdlSetPagination

#######################################################################################
class scCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.scComment
        #fields = ( 'username', 'first_name','last_name','email','date_joined')
    def create(self, validated_data):
        return models.scComment.objects.create(**validated_data)
# ViewSets define the view behavior.
class scCommentViewSet(viewsets.ModelViewSet):
    queryset = models.scComment.objects.all()
    serializer_class = scCommentSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('uid','wid')
    pagination_class = mdlSetPagination

    def create(self, request):

        wid = request.POST['wid']
        content = models.scContent.objects.get(pk=wid)
        content.comment_counts = content.comment_counts + 1
        content.save()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#######################################################################################
class scMessageSerializer(serializers.ModelSerializer):
    uid_name = serializers.ReadOnlyField(source='uid.nickname')
    uid_avator = serializers.ReadOnlyField(source='uid.user_image.url')
    uid2_name = serializers.ReadOnlyField(source='uid2.nickname')
    uid2_avator = serializers.ReadOnlyField(source='uid2.user_image.url')
    class Meta:
        model = models.scMessage
        fields = ( 'pk','uid','uid2','text', 'time','uid_name','uid2_name','uid_avator','uid2_avator')
    def create(self, validated_data):
        return models.scMessage.objects.create(**validated_data)
# ViewSets define the view behavior.
class scMessageViewSet(viewsets.ModelViewSet):
    queryset = models.scMessage.objects.all()
    serializer_class = scMessageSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser, MultiPartParser, )
    filter_fields = ('uid','uid2')
    pagination_class = mdlSetPagination
#######################################################################################
#######################################################################################



