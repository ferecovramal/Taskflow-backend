from rest_framework.permissions import BasePermission, SAFE_METHODS



  #YALNIZ ADMIN OLAN USER'E ICAZE VEREN PERMISSIONS HISSE
class IsOrganizationAdmin(BasePermission):
    def has_permission(self, request, view):
        #EGER USER LOGIN OLUBSA VE ADMIN-DISE ICAZE VAR
        return request.user.is_authenticated and request.user.is_admin


    #SADECE OXUMAGA ICAZER VEREN PERMISSIONS HISSE
class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        #EGER METOD GET-DIRSE ICAZE VERILIR
        if request.method in SAFE_METHODS:
            return True
        #EKS HALDA (PUT,POST,DELETE) ICAZE YOXDUR
        return False


    #EYNI ORGANIZATION DAXILINDE ISLEMEYE ICAZE VEREN PERMISSION
class IsSameOrganization(BasePermission):
    def has_object_permission(self, request, view, obj):
        #SUPERUSER ISTENILEN MELUMATI GORE BILER
        if request.user.is_superuser:
            return True
        #YALNIZ EYNI ORGANIZATION-A AID MELUMATLARA ICAZE VER
        return obj.organization == request.user.organization


    #YALNIZ OZ TASKINI GORE BILER VE DEYISE BILER
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        #SuperAdmin her seyi gore ve deyise biler
        if request.user.is_superuser:
            return True

        #Oxumaq (GET) icazesi
        if request.method in SAFE_METHODS:
            #Organization daxili butun userler task'i oxuya biler
            return obj.organization == request.user.organization

        #Read/Update/Delete icazesi
        #Yalniz: Organization admin, Task'a assigned user
        if request.user.is_admin:
            return True

        #Assigned user yoxlanir
        return request.user in obj.assigned_users.all()


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsOwnerOrAdminOrSuperAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if user.is_admin and obj.organization == user.organization:
            return True

        return obj.id == user.id


class CanChangeTaskStatus(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_admin:
            return True
        return request.user in obj.assigned_users.all()
