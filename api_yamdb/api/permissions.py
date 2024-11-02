from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    """
    Custom permissions for object access:
    - Allows safe methods for all users.
    - Allows all methods for authenticated users.
    - Only the object author, moderators, and admins can modify or delete the object.
    """
   
    def has_permission(self, request, view):
       # Allow safe methods for all users
       if request.method in permissions.SAFE_METHODS:
            return True
       
       # Allow other methods only for authenticated users
       return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for unauthenticated users
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        
        # Allow safe methods for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the object has an 'author' attribute
        if hasattr(obj, 'author'):
            # Allow modifications for the author, moderators, and admins
            return obj.author == request.user or request.user.role in ('moderator', 'admin')
        
        # Allow modifications for moderators and admins if no 'author' attribute
        return request.user.role in ('moderator', 'admin')
