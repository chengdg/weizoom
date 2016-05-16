__author__ = 'bert'
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

print type(sys.argv)
print sys.argv
execute_from_command_line([sys.argv[0]])

from django.conf import settings
from modules.member.models import *
from account.social_account.models import SocialAccount
from weixin.user.models import WeixinUser
#from market_tools.tools.channel_qrcode.models import * 

import time

# members = Member.objects.filter(shop_name=3211)
# myfile = open('list.txt','wb')
# for member in members:
#   id = member.id

#   member_relations = MemberFollowRelation.objects.filter(member_id=id)
#   name_list = []
#   name_list.append(member.username)
#   for member_relation in member_relations:
#       try:
#           follower_member = Member.objects.get(id=member_relation.follower_member_id)
#           if follower_member.username.strip() != '':
#               name_list.append(follower_member.username)

#       except Exception, e:
#           raise e

#   myfile.write(','.join(name_list)+'\n')

# myfile.close()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print 'please command: python remove_member 1'
        sys.exit(0)
    member_id = sys.argv[1].split(',')



    MemberSharedUrlInfo.objects.filter(member_id__in=member_id).delete()

    MemberFollowRelation.objects.filter(member_id__in=member_id).delete()
    MemberFollowRelation.objects.filter(follower_member_id__in=member_id).delete()

    MemberBrowseRecord.objects.filter(member_id__in=member_id).delete()

    MemberHasTag.objects.filter(member_id__in=member_id).delete()

    MemberInfo.objects.filter(member_id__in=member_id).delete()

    member_has_socials = MemberHasSocialAccount.objects.filter(member_id__in=member_id)

    for member_has_social in member_has_socials:
        try:
            SocialAccount.objects.filter(id=member_has_social.account.id).delete()
            WeixinUser.objects.filter(username=member_has_social.account.openid)
        except:
            pass


    MemberHasSocialAccount.objects.filter(member_id__in=member_id).delete()

    WebAppUser.objects.filter(member_id__in=member_id).delete()
    #ChannelQrcodeHasMember.objects.filter(member_id__in=member_id).delete()
    Member.objects.filter(id__in=member_id).delete()