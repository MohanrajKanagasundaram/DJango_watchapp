from rest_framework import permissions

class AdminReadOnly(permissions.IsAdminUser):
    def has_permission(self,request,method):
        
       if request.method in permissions.SAFE_METHODS:
           return True
       else:
           return request.user and request.user.is_admin_user
       
class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user==request.user
        
    