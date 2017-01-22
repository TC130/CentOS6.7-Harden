#coding:utf-8
import os
import re

# ######################################
# #1.shadow加密状态检查
# ######################################
res = os.popen("authconfig --test|grep hashing").read()
#print res
if "sha512" in res:
    print "1.shadow加密目前安全!"
else:
    print "1.warning:加密算法不是sha512，不安全"
    #执行加固
    os.system("authconfig --passalgo=sha512 --update")
#
#
# ######################################
# #2.Root直接登录检查
# ######################################
res = os.popen("cat /etc/ssh/sshd_config | grep PermitRootLogin").read()
# print res
if "#PermitRootLogin no" in res:
    print "2.当前Root允许直接登录，不安全"
    os.system("sed -i 's&#PermitRootLogin no&PermitRootLogin no&g' /etc/ssh/sshd_config")
    print os.popen("cat /etc/ssh/sshd_config | grep PermitRootLogin").read()
    os.system("/etc/init.d/sshd restart")
elif "#PermitRootLogin yes" in res:
    print "2.当前Root允许直接登录，不安全"
    os.system("sed -i 's&#PermitRootLogin yes&PermitRootLogin no&g' /etc/ssh/sshd_config")
    print os.popen("cat /etc/ssh/sshd_config | grep PermitRootLogin").read()
    os.system("/etc/init.d/sshd restart")
elif "PermitRootLogin yes" in res:
    print "2.当前Root允许直接登录，不安全"
    os.system("sed -i 's&PermitRootLogin yes&PermitRootLogin no&g' /etc/ssh/sshd_config")
    print os.popen("cat /etc/ssh/sshd_config | grep PermitRootLogin").read()
    os.system("/etc/init.d/sshd restart")
elif "PermitRootLogin no" in res:
    print "2.Root不允许直接登录，安全"
else:
    print "2.Something Wrong"
#
#
# ######################################
# #3.远程登录检查
# ######################################
res = os.popen("cat /etc/securetty").read()
# print res
if "#CONSOLE=" in res:
    print "3.当前允许root直接登录，不安全"
    os.system("sed -i 's&#CONSOLE&CONSOLE&g' /etc/securetty")

elif "CONSOLE=" in res:
    print "3.安全"
else:
    print "3.根本就没有关于CONSOLE的字段，直接添加了"
    os.system("sed -i '1i\CONSOLE=/dev/tty01' /etc/securetty")

######################################
#4.添加到sudo 目前用不到，用到时启用即可
######################################
# #让用户输入一个账户名
# user = raw_input("请输入要添加到suduer的用户名:")
#
# #先检查是否有这个用户
# res = os.popen("cat /etc/passwd").read()
# print res
# if user in res:
#     # 添加到sudo文件中
#     print "ok"
#     os.system("sed '/^root/a\'"+user+"'\tALL=(ALL)\tALL' /etc/sudoers")
#
# else:
#     #todo 添加新用户 后续再说了
#     print "不在用户列表中"



######################################
#5.设置口令策略
######################################
res = os.popen("cat /etc/login.defs|grep PASS").read()
print "4.加固前状态如下："
print res

#先注释 之后再写新一行



os.system("sed -i 's&^PASS_MAX_DAYS&#PASS_MAX_DAYS&g' /etc/login.defs")
os.system("sed -i '/^#PASS_MAX_DAYS/a\PASS_MAX_DAYS 90' /etc/login.defs")

os.system("sed -i 's&^PASS_MIN_DAYS&#PASS_MIN_DAYS&g' /etc/login.defs")
os.system("sed -i '/^#PASS_MIN_DAYS/a\PASS_MIN_DAYS 0' /etc/login.defs")

os.system("sed -i 's&^PASS_WARN_AGE&#PASS_WARN_AGE&g' /etc/login.defs")
os.system("sed -i '/^#PASS_WARN_AGE/a\PASS_WARN_AGE 7' /etc/login.defs")

os.system("sed -i 's&^PASS_MIN_LEN&#PASS_MIN_LEN&g' /etc/login.defs")
os.system("sed -i '/^#PASS_MIN_LEN/a\PASS_MIN_LEN 8' /etc/login.defs")
res = os.popen("cat /etc/login.defs|grep PASS").read()
print "4.加固后的状态如下："
print res

os.system("sed -i 's&^password\s*requisite\s*pam_cracklib.so&#password    requisite     pam_cracklib.so&g' /etc/pam.d/system-auth")
os.system("sed -i '/^#password\s*requisite\s*pam_cracklib.so/a\password    requisite     pam_cracklib.so minlen=8 retry=5 ucredit=-1 lcredit=-1 ocredit=-1 dcredit=-1' /etc/pam.d/system-auth")

######################################
#6.设置自动注销时间
######################################
res = os.popen("cat /etc/profile|grep TMOUT").read()
if res=="":
    print "5.当前超时时间："
    print "永不超时"
else:
    print "5.当前超时时间："
    print res
if "TMOUT" in res:
    os.system("sed -i 's&^TMOUT&#TMOUT&g' /etc/profile")
    os.system("echo 'TMOUT=600' >>/etc/profile")
else:
    os.system("echo 'TMOUT=600' >>/etc/profile")

os.system("source /etc/profile")
res = os.popen("cat /etc/profile|grep TMOUT").read()
print "5.更新后的超时时间"
print res

######################################
#7.设置Bash保留历史命令的条数 只记录5条
######################################
res = os.popen("cat /etc/profile|grep HISTSIZE").read()

if "HISTSIZE=" in res:
    print "6.当前记录的命令行数目"
    print res
    os.system("sed -i 's&^HISTSIZE=&#HISTSIZE=&g' /etc/profile")
    os.system("echo 'HISTSIZE=5' >>/etc/profile")
else:
    os.system("echo 'HISTSIZE=5' >>/etc/profile")

os.system("source /etc/profile")
res = os.popen("cat /etc/profile|grep HISTSIZE").read()
print "6.更新后的记录的命令行数目"
print res

######################################
#8.禁用ctrl alt delete
######################################
res = os.popen("cat /etc/init/control-alt-delete.conf").read()
# print res
if "#exec" not in res:
    print "6.当前允许ctrl alt del，不安全"
    print res
    os.system("sed -i 's&^exec&#exec&g' /etc/init/control-alt-delete.conf")

res = os.popen("cat /etc/init/control-alt-delete.conf").read()
# print res
if "#exec" in res:
    print "6.当前已禁止ctrl alt del，安全"
    print res

######################################
#9.检查用户列表
######################################
res = os.popen("awk -F: '{print $1}' /etc/passwd").read()
print "当前用户列表："
print res
print "请检查上述用户是否有异常！"
######################################
#10.启用证书登录(二期再做）
######################################
# #todo 执行ssh keygen 放在最后一步就行
# os.system("ssh-keygen -t rsa")
#
# #改文件名
# os.system("mv /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys")
# os.system("chmod 400 authorized_keys")
# res = os.popen("cat /etc/ssh/sshd_config").read()
# print res
# #修改sshd_config
# 修改 / etc / ssh / sshd_config，启用证书登录，不允许密码登录
# RSAAuthentication yes
# PubkeyAuthentication yes
# AuthorizedKeysFile .ssh/authorized_keys
# PasswordAuthentication no
##todo 把私钥文件导出
#
#







