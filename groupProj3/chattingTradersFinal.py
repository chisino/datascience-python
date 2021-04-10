import pandas as pd
from operator import itemgetter
import matplotlib.pyplot as plt

def GetData():

   with open("users.tsv") as users:
       UserData = pd.read_csv(users,delimiter='\t')
   with open("messages.tsv") as messages:
       MessageData = pd.read_csv(messages, delimiter='\t')
   with open("discussions.tsv") as discussions:
       DiscussionData = pd.read_csv(discussions, delimiter='\t')
   with open("discussion_posts.tsv") as posts:
       PostData = pd.read_csv(posts, delimiter='\t')

   return UserData, MessageData, DiscussionData, PostData #returns four dataframes


def GetIds(RawData):
   UserData = RawData[0]
   MessageData = RawData[1]
   DiscussionData = RawData[2]
   PostData = RawData[3]
   AssociatedFrames = {}
   ListOfUserId = list(UserData['id'])
   TotalUsers = len(ListOfUserId)

   for X in ListOfUserId:
       MessagesSent = MessageData.loc[MessageData['sender_id'] == X]
       DiscussionCreated = DiscussionData.loc[DiscussionData['creator_id'] == X]
       PostCreated = PostData.loc[PostData['creator_id'] == X]
       AssociatedFrames[X] = [MessagesSent, DiscussionCreated, PostCreated]

   return TotalUsers, AssociatedFrames

def GetActivityRange(UA):
   TimeBetween = []
   Users = list(UA.keys())
   for X in Users:
       Max = UA[X][0]['sendDate'].max()
       Min = UA[X][0]['sendDate'].min()
       if Max != Min and Max > Min:
           TimeBetween.append((Max - Min)/ (1000 * 60 * 60 * 24))
   return TimeBetween

def GetActivityDelay(UD, UA):
   Users = list(UA.keys())
   MessageTypes = UA[1][0].type.unique()
   UActivity = []
   for X in Users:
       CreationDate = int(UD.loc[UD['id'] == X]['memberSince']) / (1000 * 60 * 60 * 24)
       for Z in MessageTypes:
           FirstActivity = UA[X][0].loc[UA[X][0]['type'] == Z]['sendDate'].min() / (1000 * 60 * 60 * 24)
           if FirstActivity != CreationDate and CreationDate < FirstActivity:
               UActivity.append(int(FirstActivity - CreationDate))
   return UActivity

def DiscussionDistribution(Data):
   DiscussionData = Data[2]

   DiscussionTypes = DiscussionData.discussionCategory.unique()
   Popularity = []
   for X in DiscussionTypes:
       TotalPosts = len(DiscussionData.loc[DiscussionData['discussionCategory'] == X])
       Popularity.append([X,TotalPosts])

   Popularity = sorted(Popularity, key=itemgetter(1)) #StackOverflow
   return Popularity

def GetPostActivityDelay(UD, UA):
   Users = UD[0]['id']
   MostPopular = UA[-1][0]
   MostPopular = UD[2].loc[UD[2]['discussionCategory'] == MostPopular]
   UActivity = []
   for X in Users:
       CreationDate = int(UD[0].loc[UD[0]['id'] == X]['memberSince']) / (1000 * 60 * 60 * 24)
       FirstActivity = MostPopular.loc[MostPopular['creator_id'] == X]['createDate'].min() / (1000 * 60 * 60 * 24)
       if FirstActivity != CreationDate and CreationDate < FirstActivity:
           UActivity.append(int(FirstActivity - CreationDate))
   return UActivity



def DisplayActivityRange(activityRange):
   plt.hist(activityRange)

   plt.title("Activity Range")
   plt.ylabel('Number of Users')
   plt.xlabel('Delay in days')
   plt.savefig("Q_2.png", dpi=200)
   plt.clf()


def DisplayActivityDelay(activityDelay):
   plt.hist(activityDelay)
   plt.title("Activity Delay")
   plt.ylabel('Number of Users')
   plt.xlabel('Delay in days')
   plt.savefig("Q_3.png", dpi=200)
   plt.clf()

def DisplayPostActivityDelay(postActivityDelay):
   plt.hist(postActivityDelay)
   plt.title("Post Activity Delay")
   plt.ylabel('Number of Users')
   plt.xlabel('Delay in days')
   plt.savefig("Q_5.png", dpi=200)
   plt.clf()
def SimpleDeliverables(Info):
  discMax = Info[2].createDate.max()
  discMin = Info[2].createDate.min()
  postMax = Info[3].createDate.max()
  postMin = Info[3].createDate.min()


  if (discMax > postMax):
   maxTime = discMax
  else:
   maxTime = postMax

  if (discMin > postMin):
   minTime = discMin
  else:
   minTime = postMin

  timeSpan = ((maxTime - minTime) / (1000 * 60 * 60 * 24))  # convert milliseconds to days

  print("The Database has a timespan of: "+ str(timeSpan) +" days." )

  msgTypeDict = Info[1].type.value_counts().to_dict()

  plt.pie(list(msgTypeDict.values()))
  plt.title("Messages of Each Type")
  plt.legend(list(msgTypeDict.keys()), loc = "best")
  plt.tight_layout()

  plt.savefig("Q1_3.png", dpi=200)
  plt.clf()

  discTypeDict = Info[2].discussionCategory.value_counts().to_dict()

  plt.pie(list(discTypeDict.values()))
  plt.title("Discussions of Each Type")
  plt.legend(list(discTypeDict.keys()), loc = "best")
  plt.tight_layout()

  plt.savefig("Q1_4.png", dpi=200)
  plt.clf()

  print("This database contains a total of: " + str(Info[3].count().tolist()[0]) + " discussion posts")

def DisplayDiscussionDistribution(popularity):
  popVals = []
  popLabels = []

  for i in popularity:
   popVals.append(i[1])
   popLabels.append(i[0])

  explode = (0, 0, 0, 0, 0, 0, 0, 0, 0.1)

  plt.pie(popVals, explode=explode)
  plt.title("Discussion Distribution")
  plt.legend(popLabels, loc = "best")
  plt.tight_layout()

  plt.savefig("Q_4.png", dpi=200)
  plt.clf()


def main():
   Info = GetData()  # gets dataframes, will be used to extract useful information
   TotalUsers, UserActivity = GetIds(Info)
   ActivityRange = GetActivityRange(UserActivity)
   ActivityDelay = GetActivityDelay(Info[0], UserActivity)
   PostDistribution = DiscussionDistribution(Info)
   postActivityDelay = GetPostActivityDelay(Info, PostDistribution)
   print("There are " + str(TotalUsers) +" known users.")
   SimpleDeliverables(Info)
   DisplayPostActivityDelay(postActivityDelay)
   DisplayDiscussionDistribution(PostDistribution)
   DisplayActivityRange(ActivityRange)
   DisplayActivityDelay(ActivityDelay)

main()
