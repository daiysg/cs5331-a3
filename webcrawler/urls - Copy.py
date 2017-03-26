URLs = {}

# add these into the site's dictionary if you want to override it on
# the site level
crawl_rules_allow=()
crawl_rules_deny=("\#",
                  ".*=del.*",
                  ".*logout.*",
                  ".*page=.*",
                  ".*calendar.php\?date=1.*",
                  ".*administrator.php\?ctg=calendar&view_calendar=.*",
                  ".*search/search?term=.*",
                  ".*sesskey=.*",
                  ".*cache/testperformance.php?.*")

                  
# values to try out for certain parameters
paramtype_test_input = {"password":["mypassword"]}
paramname_test_input = {"currency_code":["USD"]}


URLs["https://app4.com"] = {"name":"app4_admin",
                            "login_page":"https://app4.com/index.php",
                            "need_selenium" : False,
                            "formnumber":1,
                            "formdata":{'username': 'admin@admin.com', 'password': 'admin'},}

# admin
URLs["https://app6.com"] = {"name":"app6_admin",
                            "login_page":"https://app6.com/zimplit.php?action=login",
                            "need_selenium" : False,
                            "formnumber":0,
                            "formdata":{'username': 'admin', 'password': 'admin'},}

# regular
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


# admin
URLs["https://app1.com/admin"] = {"name":"app1_admin",
                                  "need_selenium" : False,
                                  "login_page":"https://app1.com/admin/index.php?page=login",
                                  "formnumber":0,
                                  "formdata":{'adminname': 'admin', 'password': 'admin'},}
# regular
URLs["https://app1.com"] = {"name":"app1_user",
                            "need_selenium" : False,
                            "login_page":"https://app1.com/users/login.php",
                            "formnumber":1,
                            "formdata":{'username': 'scanner1', 'password': 'scanner1'},}

# admin
URLs["https://app2.com"] = {"name":"app2_admin",
                            "need_selenium" : False,
                            "login_page":"https://app2.com/login/index.php",
                            "formxpath":"//form[@id='login']",
                            "formdata":{'username': 'admin', 'password': 'AdminAdmin1!'},}

URLs["https://app3.com"] = {"name":"app3",
                            "need_selenium" : False,}

# admin
URLs["https://app5.com/www"] = {"name":"app5_admin",
                                "need_selenium" : True,
                                "login_page":"https://app5.com/www/index.php",
                                "formxpath":"//form[@id='login_form']",
                                "formdata":{'login': 'admin', 'password': 'admin'},}

# admin
URLs["https://app7.com/oc-admin"] = {"name":"app7_admin",
                                     "need_selenium" : False,
                                     "login_page":"https://app7.com/oc-admin/index.php?page=login",
                                     "formxpath":"//form[@id='loginform']",
                                     "formdata":{'user_login': 'admin', 'user_pass': 'admin'},}                                         

# admin
URLs["https://app7.com"] = {"name":"app7_user",
                            "need_selenium" : False,
                            "login_page":"https://app7.com/index.php?page=login",
                            "formnumber":0,
                            "formdata":{'email': 'test@test.com', 'password': 'testtest'},}    

# admin
URLs["https://app9.com/index-test.php"] = {"name":"app9_admin",
                                           "need_selenium" : False,
                                           "login_page":"https://app9.com/index-test.php/site/login",
                                           "formxpath":"//form[@id='yw0']",
                                           "formdata":{'LoginForm[username]': 'admin', 'LoginForm[password]': 'admin'},}    


URLs["https://app10.com"] = {"name":"app10",
                             "need_selenium" : False,}

# admin
URLs["https://app11.com/ajaxfilemanager.php"] = {"name":"app11_admin",
                                                 "need_selenium" : False,
                                                 "login_page":"https://app11.com/ajax_login.php",
                                                 "formxpath":"//form[@name='frmLogin']",
                                                 "formdata":{'username': 'admin', 'password': 'admin'},}    

# Self Benchmarks
# Case 01 admin
URLs["https://bm1.com/case01"] = {"name":"sb_case01",
                                  "need_selenium" : False,
                                  "login_page":"https://bm1.com/case01/login.php",
                                  "formxpath":"//form[@name='login_form']",
                                  "formdata":{'username': 'admin', 'password': 'admin'},}    

# Case 02 admin
URLs["https://bm1.com/case02"] = {"name":"sb_case02",
                                  "need_selenium" : False,
                                  "login_page":"https://bm1.com/case02/login.php",
                                  "formxpath":"//form[@name='login_form']",
                                  "formdata":{'username': 'admin', 'password': 'admin'},}    

# X2Engine
URLs["https://bm1.com/X2CRM/x2engine/index.php/site/login"] = {"name":"sb_x2engine",
                                          "need_selenium" : False,
                                          "login_page":"https://bm1.com/X2CRM/x2engine/index.php/site/login",
                                          "formxpath":"//form[@id='yw0']",
                                          "formdata":{'LoginForm[username]': 'admin', 'LoginForm[password]': 'admin'},}    
   
# Cubecart
URLs["https://bm1.com/cubecart"] = {"name":"sb_cubecart",
                                    "need_selenium" : False,
                                    "login_page":"https://bm1.com/cubecart/admin.php",
                                    "formnumber":0,
                                    "formdata":{'username': 'admin', 'password': 'admin'},}    
   
# Grawlix
URLs["https://bm1.com/grawlix/_admin"] = {"name":"sb_grawlix",
                                          "need_selenium" : False,
                                          "login_page":"https://bm1.com/grawlix/_admin/panl.login.php",
                                          "formnumber":0,
                                          "formdata":{'username': 'admin', 'password': 'admin'},}   


# iTop (Clean)
URLs["https://bm1.com/itop-clean/web/pages"] = {"name":"sb_itop",
                                                "need_selenium" : False,
                                                "login_page":"http://bm1.com/itop-clean/web/pages/UI.php",
                                                "formnumber":0,
                                                "formdata":{'auth_user': 'admin', 'auth_pwd': 'admin'},} 

# Opendocman
URLs["https://bm1.com/opendocman"] = {"name":"sb_opendocman",
                                      "need_selenium" : False,
                                      "login_page":"https://bm1.com/opendocman",
                                      "formnumber":0,
                                      "formdata":{'frmuser': 'admin', 'frmpass': 'admin'},} 

# PHP Server Monitor admin
URLs["https://bm1.com/phpservermon"] = {"name":"sb_phpservermon_admin",
                                        "need_selenium" : False,
                                        "login_page":"https://bm1.com/phpservermon",
                                        "formnumber":0,
                                        "formdata":{'user_name': 'admin', 'user_password': 'admin'},} 

# PHP Server Monitor user
URLs["https://bm1.com/phpservermon"] = {"name":"sb_phpservermon_user",
                                        "need_selenium" : False,
                                        "login_page":"https://bm1.com/phpservermon",
                                        "formnumber":0,
                                        "formdata":{'user_name': 'user', 'user_password': 'user'},} 

# Pligg
URLs["https://bm1.com/pligg-cms-master"] = {"name":"sb_pligg",
                                            "need_selenium" : True,
                                            "login_page":"http://bm1.com/pligg-cms-master/login.php",
                                            "formxpath":"//form[@id='thisform']/form",
                                            "formdata":{'username': 'admin', 'password': 'admin'},} 

# Testlink
URLs["https://bm1.com/testlink"] = {"name":"sb_testlink",
                                    "need_selenium" : False,
                                    "login_page":"http://bm1.com/testlink/login.php",
                                    "formxpath":"//form[@name='login_form']",
                                    "formdata":{'tl_login': 'admin', 'tl_password': 'admin'},} 

# Xoops
URLs["https://bm1.com/xoops/htdocs"] = {"name":"sb_xoops",
                                        "need_selenium" : False,
                                        "login_page":"https://bm1.com/xoops/htdocs",
                                        "formnumber":0,
                                        "formdata":{'uname': 'admin', 'password': 'admin'},} 
