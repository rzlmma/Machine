
[开发指南]

# 权限管理


用户可以有多个角色
角色可以绑定多个权限
权限的codename作为装饰器的参数


## 后台权限：
在函数前加上装饰器，检验当前登陆用户是否有执行该动作的权限，
示例见 system.tests.permission_test_case


## 前端权限：
用户登陆时从数据库获取其许可项和禁用项列表，存入服务端session，
权限里已添加各个菜单的codename, 页面加载时从session获取该用户的许可项或禁用项
见 system.views.get_session_disable 和 system.views.get_session_permit

左边导航栏菜单默认全隐藏，每个菜单项有一个PERM_CODE="xxx"属性
加载页面时取得用户的许可项，将菜单设置为显示
见 templates/nav.html
