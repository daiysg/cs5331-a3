URLs = {}

# add these into the site's dictionary if you want to override it on
# the site level
crawl_rules_allow = ()
crawl_rules_deny = ("\#",
                    ".*=del.*",
                    ".*logout.*",
                    ".*page=.*",
                    ".*calendar.php\?date=1.*",
                    ".*administrator.php\?ctg=calendar&view_calendar=.*",
                    ".*search/search?term=.*",
                    ".*sesskey=.*",
                    ".*cache/testperformance.php?.*")

# values to try out for certain parameters
paramtype_test_input = {"password": ["mypassword"]}
paramname_test_input = {"currency_code": ["USD"]}

# URLs["https://app1.com/admin/index.php?page=login"] = {"name":"app1_admin",
#     "login_page":"https://app1.com/admin/index.php?page=login",
#     "need_selenium" : False,
#     "formnumber":1,
#     "formdata":{'adminname': 'admin', 'password': 'admin'},}
#
# URLs["https://app1.com/admin/index.php?page=login"] = {"name":"app1_adamd",
#     "login_page":"https://app1.com/admin/index.php?page=login",
#     "need_selenium" : False,
#     "formnumber":1,
#     "formdata":{'username': 'adamd', 'password': 'adamd'},}
#
# URLs["https://app1.com/users/login.php"] = {"name":"app1_scanner1",
#     "login_page":"https://app1.com/users/login.php",
#     "need_selenium" : False,
#     "formnumber":2,
#     "formdata":{'username': 'scanner1', 'password': 'scanner1'},}
#
# URLs["https://app1.com/users/login.php"] = {"name":"app1_scanner2",
#     "login_page":"https://app1.com/users/login.php",
#     "need_selenium" : False,
#     "formnumber":2,
#     "formdata":{'username': 'scanner2', 'password': 'scanner2'},}
#
# URLs["https://app1.com/users/login.php"] = {"name":"app1_bryce",
#     "login_page":"https://app1.com/users/login.php",
#     "need_selenium" : False,
#     "formnumber":2,
#     "formdata":{'username': 'bryce', 'password': 'bryce'},}

# URLs["https://app2.com/files/news.php"] = {"name":"app2_admin",
#     "login_page":"https://app2.com/files/news.php",
#     "need_selenium" : False,
#     "formnumber":1,
#     "formdata":{'username': 'admin', 'password': 'adminadmin'},}
#
# URLs["https://app3.com/admins"] = {"name":"app3_admin",
#     "login_page":"https://app3.com/admins",
#     "need_selenium" : False,
#     "formnumber":1,
#     "formdata":{'username': 'admin', 'password': 'admin'},}
#
# URLs["https://app3.com"] = {"name":"app3_test",
#     "login_page":"https://app3.com",
#     "need_selenium" : False,
#     "formnumber":1,
#     "formdata":{'username': 'test@test.com', 'password': 'testtest'},}
#
URLs["https://app4.com/catalog/admin/"] = {"name": "app4_admin",
                                           "login_page": "https://app4.com/catalog/admin/",
                                           "need_selenium": False,
                                           "formnumber": 1,
                                           "formdata": {'username': 'admin', 'password': 'admin'}, }

URLs["https://app4.com/catalog"] = {"name": "app4_test",
                                    "login_page": "https://app4.com/catalog/",
                                    "need_selenium": True,
                                    "formnumber": 1,
                                    "formdata": {'username': 'test@test.com', 'password': 'testtest'}, }

# URLs["https://app5.com/"] = {"name":"app5_admin",
#     "login_page":"https://app5.com/",
#     "need_selenium" : False,
#     "formnumber":1,
#     "formdata":{'username': 'admin', 'password': 'adminadmin'},}

URLs["https://app6.com/admin.php"] = {"name": "app6_admin",
                                      "login_page": "https://app6.com/admin.php",
                                      "need_selenium": False,
                                      "formnumber": 1,
                                      "formdata": {'username': 'admin', 'password': 'adminadmin'}, }

URLs["https://app6.com/"] = {"name": "app6_user",
                             "login_page": "https://app6.com",
                             "need_selenium": False,
                             "formnumber": 1,
                             "formdata": {'username': 'admin', 'password': 'adminadmin'}, }
#
# URLs["https://app7.com/"] = {"name":"app7_test",
#     "login_page":"https://app7.com/index.php?page=login",
#     "need_selenium" : False,
#     "formnumber":0,
#     "formdata":{'email': 'test@test.com', 'password': 'testtest'},}
#
# URLs["https://app7.com/oc-admin/index.php"] = {"name":"app7_admin",
#     "login_page":"https://app7.com/oc-admin/index.php?page=login",
#     "need_selenium" : False,
#     "formxpath":"//form[@id='loginform']",
#      "formdata":{'user_login': 'admin', 'user_pass': 'admin'},}
#
# # regular
URLs["https://app8.com/upload"] = {"name":"app8_user",
                                   "need_selenium" : True,
                                   "login_page":"https://app8.com/upload/index.php?route=account/login",
                                   "formxpath":"//form[@id='login']",
                                   "formdata":{'email': 'test@test.com', 'password': 'test'},}

# admin
URLs["https://app8.com/upload/admin"] = {"name":"app8_admin",
                                         "need_selenium" : True,
                                         "login_page":"https://app8.com/upload/admin/index.php",
                                         "formxpath":"//form[@id='form']",
                                         "formdata":{'username': 'admin', 'password': 'admin'},}
#
# # admin
# URLs["https://app9.com/index-test.php"] = {"name":"app9_admin",
#                                            "need_selenium" : False,
#                                            "login_page":"https://app9.com/index-test.php/site/login",
#                                            "formxpath":"//form[@id='yw0']",
#                                            "formdata":{'LoginForm[username]': 'admin', 'LoginForm[password]': 'admin'},}
#
# # admin
# URLs["https://app9.com/index-test.php"] = {"name":"app9_test",
#                                            "need_selenium" : False,
#                                            "login_page":"https://app9.com/index-test.php/site/login",
#                                            "formxpath":"//form[@id='yw0']",
#                                            "formdata":{'LoginForm[username]': 'test', 'LoginForm[password]': 'test'},}
#
# URLs["https://app10.com"] = {"name":"app10",
#    "need_selenium" : False,
#    "login_page":"https://app10.com",}
#
# URLs["https://app11.com"] = {"name":"app11_test",
#    "need_selenium" : False,
#    "login_page":"https://app11.com",
#    "formxpath":"//form[@id='yw0']",
#    "formdata":{'username': 'admin', 'password': 'admin'},}
#
# # admin
# URLs["https://app12.com"] = {"name":"app12_admin",
#                             "need_selenium" : False,
#                             "login_page":"https://app12.com/login/index.php",
#                             "formxpath":"//form[@id='login']",
#                             "formdata":{'username': 'admin', 'password': 'AdminAdmin1!'},}
#
# URLs["https://app12.com"] = {"name":"app12_test",
#                             "need_selenium" : False,
#                             "login_page":"https://app12.com/login/index.php",
#                             "formxpath":"//form[@id='login']",
#                             "formdata":{'username': 'test', 'password': 'TestTest1!'},}
#
# URLs["https://app13.com"] = {"name":"app13",
#    "need_selenium" : False,
#    "login_page":"https://app13.com",}
#
# URLs["https://app14.com"] = {"name":"app14_admin",
#    "need_selenium" : False,
#    "login_page":"https://app14.com",
#    "formdata":{'username': 'admin@admin.com', 'password': 'admin'},}
#
# URLs["https://app14.com"] = {"name":"app14_developer",
#    "need_selenium" : False,
#    "login_page":"https://app14.com",
#    "formdata":{'username': 'dev@dev.com', 'password': 'developer'},}
#
# URLs["https://app14.com"] = {"name":"app14_manager",
#    "need_selenium" : False,
#    "login_page":"https://app14.com",
#    "formdata":{'username': 'manager@manager.com', 'password': 'manager'},}
#
# URLs["https://app14.com"] = {"name":"app14_user",
#    "need_selenium" : False,
#    "login_page":"https://app14.com",
#    "formdata":{'username': 'user@user.com', 'password': 'user'},}
#
# # admin
# URLs["https://app15.com/www/index.php"] = {"name":"app15_admin",
#     "need_selenium" : True,
#     "login_page":"https://app15.com/www/index.php",
#     "formxpath":"//form[@id='login_form']",
#     "formdata":{'login': 'admin', 'password': 'admin'},}
#
# URLs["https://app15.com/www/index.php"] = {"name":"app15_professor",
#     "need_selenium" : True,
#     "login_page":"https://app15.com/www/index.php",
#     "formxpath":"//form[@id='login_form']",
#     "formdata":{'login': 'professor', 'password': 'professor'},}
#
# URLs["https://app15.com/www/index.php"] = {"name":"app15_student",
#     "need_selenium" : True,
#     "login_page":"https://app15.com/www/index.php",
#     "formxpath":"//form[@id='login_form']",
#     "formdata":{'login': 'student', 'password': 'student'},}
#
# URLs["https://app15.com/www/index.php"] = {"name":"app15_student2",
#     "need_selenium" : True,
#     "login_page":"https://app15.com/www/index.php",
#     "formxpath":"//form[@id='login_form']",
#     "formdata":{'login': 'student2', 'password': 'student2'},}
#
# # admin
# URLs["https://app16.com/ajaxfilemanager.php"] = {"name":"app16_admin",
#                                                  "need_selenium" : False,
#                                                  "login_page":"https://app16.com/ajax_login.php",
#                                                  "formxpath":"//form[@name='frmLogin']",
#                                                  "formdata":{'username': 'admin', 'password': 'admin'},}
#
# URLs["https://app17.com"] = {"name":"app17_admin",
#    "need_selenium" : False,
#    "login_page":"https://app17.com",
#    "formdata":{'username': 'admin@admin.com', 'password': 'admin'},}
#
# URLs["https://app18.com"] = {"name":"app18",
#    "need_selenium" : False,
#    "login_page":"https://app18.com",}
#
# URLs["https://app18.com/wp-admin"] = {"name":"app18_admin",
#    "need_selenium" : False,
#    "login_page":"https://app18.com/wp-login.php",
#    "formdata":{'username': 'admin', 'password': 'admin'},}
#
# URLs["https://app19.com"] = {"name":"app19_admin",
#    "need_selenium" : False,
#    "login_page":"https://app19.com",
#    "formdata":{'username': 'admin', 'password': 'admin'},}
#
# URLs["https://app20.com"] = {"name":"app20",
#    "need_selenium" : False,
#    "login_page":"https://app20.com",}
#
# URLs["https://app20.com/wp-admin"] = {"name":"app20_admin",
#    "need_selenium" : False,
#    "login_page":"https://app20.com/wp-login.php",
#    "formdata":{'username': 'admin', 'password': 'admin'},}
#
# URLs["https://app21.com"] = {"name":"app21_admin",
#    "need_selenium" : False,
#    "login_page":"https://app21.com",
#    "formdata":{'username': 'admin', 'password': 'admin'},}

# Self Benchmarks
# Case 01 admin
# URLs["https://bm1.com/case01"] = {"name":"sb_case01",
# "need_selenium" : False,
# "login_page":"https://bm1.com/case01/login.php",
# "formxpath":"//form[@name='login_form']",
# "formdata":{'username': 'admin', 'password': 'admin'},}

# Case 02 admin
# URLs["https://bm1.com/case02"] = {"name":"sb_case02",
# "need_selenium" : False,
# "login_page":"https://bm1.com/case02/login.php",
# "formxpath":"//form[@name='login_form']",
# "formdata":{'username': 'admin', 'password': 'admin'},}

# X2Engine
# URLs["https://bm1.com/X2CRM/x2engine/index.php/site/login"] = {"name":"sb_x2engine",
# "need_selenium" : False,
# "login_page":"https://bm1.com/X2CRM/x2engine/index.php/site/login",
# "formxpath":"//form[@id='yw0']",
# "formdata":{'LoginForm[username]': 'admin', 'LoginForm[password]': 'admin'},}

# Cubecart
# URLs["https://bm1.com/cubecart"] = {"name":"sb_cubecart",
# "need_selenium" : False,
# "login_page":"https://bm1.com/cubecart/admin.php",
# "formnumber":0,
# "formdata":{'username': 'admin', 'password': 'admin'},}

# Grawlix
# URLs["https://bm1.com/grawlix/_admin"] = {"name":"sb_grawlix",
# "need_selenium" : False,
# "login_page":"https://bm1.com/grawlix/_admin/panl.login.php",
# "formnumber":0,
# "formdata":{'username': 'admin', 'password': 'admin'},}


# iTop (Clean)
# URLs["https://bm1.com/itop-clean/web/pages"] = {"name":"sb_itop",
# "need_selenium" : False,
# "login_page":"http://bm1.com/itop-clean/web/pages/UI.php",
# "formnumber":0,
# "formdata":{'auth_user': 'admin', 'auth_pwd': 'admin'},}

# Opendocman
# URLs["https://bm1.com/opendocman"] = {"name":"sb_opendocman",
# "need_selenium" : False,
# "login_page":"https://bm1.com/opendocman",
# "formnumber":0,
# "formdata":{'frmuser': 'admin', 'frmpass': 'admin'},}

# PHP Server Monitor admin
# URLs["https://bm1.com/phpservermon"] = {"name":"sb_phpservermon_admin",
# "need_selenium" : False,
# "login_page":"https://bm1.com/phpservermon",
# "formnumber":0,
# "formdata":{'user_name': 'admin', 'user_password': 'admin'},}

# PHP Server Monitor user
# URLs["https://bm1.com/phpservermon"] = {"name":"sb_phpservermon_user",
# "need_selenium" : False,
# "login_page":"https://bm1.com/phpservermon",
# "formnumber":0,
# "formdata":{'user_name': 'user', 'user_password': 'user'},}

# Pligg
# URLs["https://bm1.com/pligg-cms-master"] = {"name":"sb_pligg",
# "need_selenium" : True,
# "login_page":"http://bm1.com/pligg-cms-master/login.php",
# "formxpath":"//form[@id='thisform']/form",
# "formdata":{'username': 'admin', 'password': 'admin'},}

# Testlink
# URLs["https://bm1.com/testlink"] = {"name":"sb_testlink",
# "need_selenium" : False,
# "login_page":"http://bm1.com/testlink/login.php",
# "formxpath":"//form[@name='login_form']",
# "formdata":{'tl_login': 'admin', 'tl_password': 'admin'},}

# Xoops
# URLs["https://bm1.com/xoops/htdocs"] = {"name":"sb_xoops",
# "need_selenium" : False,
# "login_page":"https://bm1.com/xoops/htdocs",
# "formnumber":0,
# "formdata":{'uname': 'admin', 'password': 'admin'},}
