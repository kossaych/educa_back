from django.contrib import admin
from .models import *

admin.site.register(BaseUser)
admin.site.register(CodeVerification)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(ParentOfStudent)
 
admin.site.register(Inscription)
admin.site.register(GetOffer)
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(Group)
admin.site.register(Offer)
 
admin.site.register(Chapiter)
admin.site.register(Course)

admin.site.register(VideoComment)
admin.site.register(SummaryComment)
admin.site.register(SerieComment)
admin.site.register(CorrectionComment)
 
admin.site.register(Video)
admin.site.register(Summary)
admin.site.register(Serie)
admin.site.register(Correction)
admin.site.register(InteractiveCourseGame)
 