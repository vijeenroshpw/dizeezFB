//
//-- M O D E L S
//
var Question = Backbone.RelationalModel.extend({
  defaults : {
    text  : '',
    categories:[],
    //-- UI/Client side params
    active : false,
    answered : false
  },

  relations: [{
    type: Backbone.HasMany,
    key: 'choices',
    relatedModel: 'Choice',
    collectionType: 'ChoiceCollection',
    reverseRelation: {
      key: 'parentQuestion',
      includeInJSON: 'id'
    }
  }]
});

var Choice = Backbone.RelationalModel.extend({
  defaults: {
    correct   : 0,
    text      : '',

    //-- UI/Client side params
    active : false
  },
});


var User = Backbone.Model.extend({
  url:'/api/v1/user',
  defaults: {
    'name'    : "",
    'api_key' : ""
  },
  initialize: function() {
    this.bind('change:api_key',this.changeAPIKey);
    if(this.authenticated()){
      this.set('api_key',$.cookie('api_key'));
      this.fetch({'success':start});
    } else {
      this.save({},{'success':start});
    }
  },

  authenticated: function() {
    return Boolean($.cookie('api_key'));
  },
  changeAPIKey: function() {
    $.cookie('api_key',this.get('api_key'));
  }
});
//
//-- C O L L E C T I O N S
//
var ChoiceCollection = Backbone.Collection.extend({
  model : Choice,
  url   : '/api/v1/choices'
});

var QuestionCollection = Backbone.Collection.extend({
  model : Question,
  url   : '/api/v1/questions'
});

//
//-- V I E W S
//

var UserView = Backbone.View.extend({
  template:$('#user-template').html(),
  el:'#user-info',
  render:function(user_data) {
    compiledTemplate = _.template(this.template,user_data);
    this.$el.html(compiledTemplate);
  }
});

var LevelView = Backbone.View.extend({
  template:$('#levelinfo-template').html(),
  el:'.level-info',
  render:function(level_info) {
    compiledTemplate = _.template(this.template,level_info);
    this.$el.html(compiledTemplate);
  }
});

var ChoiceView = Backbone.Marionette.ItemView.extend({
  template : '#choice-template',
  tagName   : 'label',
  className : 'radio',

  events : {
    'change input' : 'changedAnswer'
  },

  //-- Events
  changedAnswer : function() {
    var old_answer = this.model.collection.findWhere({active:true});
    if(old_answer) {
      old_answer.set({'active' : false}, {silent : true});
    }
    //Mousetrap.trigger('down');
    this.model.get('parentQuestion').set('answered', true);
    this.model.save({'active' : true});
    //Mousetrap.trigger('down');
    gameOver(this.model);                  //-- Checks to see if game ended
  }
});

var ChoiceCollectionView = Backbone.Marionette.CollectionView.extend({
  itemView  : ChoiceView,

  initialize : function(options) {
    this.collection.bind('change:active', this.render, this)
  }
});

var QuestionItemView = Backbone.Marionette.ItemView.extend({
  template : '#question-item-template',
  tagName : 'li',

  events : {
    'click' : function() { this.model.set('active', true) }
  },

});

var QuestionCollectionView = Backbone.Marionette.CollectionView.extend({
  itemView: QuestionItemView,

  initialize : function() {
    this.collection.bind('change:active', this.render, this);
    this.collection.bind('change:answered', this.render, this);
  }
});

var QuestionView = Backbone.Marionette.Layout.extend({
  template : '#question-template',

  regions : {
    choices : '#choices'
  },

  onRender : function() {
    this.model.set('active', true);
    this.choices.show( new ChoiceCollectionView({collection : this.model.get('choices')}) )
  },

  onClose : function() {
    this.model.set({'active' : false}, {silent : true});
  }

});

var ScoreView = Backbone.Marionette.ItemView.extend({
  template : '#game-score-template',
  templateHelpers : function() { return this.options },

  initialize : function(options) {
    //-- This collection is a list of Choices
    this.collection.bind('change:active', this.render, this);
    this.collection.bind('change:answered', this.render, this);
  },
});

var GameView = Backbone.Marionette.Layout.extend({
  template : '#game-template',

  regions : {
    question  : '.game.question',
    list      : '.game.list ol',
    score     : '.game.score'
  },

  initialize : function(options) {
    this.collection.bind('change:active', this.swapQuestions, this);
  },

  onRender : function() {
    var self = this;
    this.question.show( new QuestionView({model : this.collection.at(0)}) );
    this.list.show( new QuestionCollectionView(this.options) );
    //this.score.show( new ScoreView({collection : new ChoiceCollection(_.flatten(_.map(self.collection.pluck('choices'), function(collection) { return collection.models }))) }) );

    Mousetrap.bind(['down', 'right'], function() { self.loop(1); });
    Mousetrap.bind(['up', 'left'], function() { self.loop(-1); })
  },

  onClose : function() {
    Mousetrap.unbind(['up', 'right', 'down', 'left']);
  },

  //-- Events
  loop : function(dir) {
    var index = this.collection.indexOf( this.collection.findWhere({active:true}) ) + dir,
        index = (index < 0) ? this.collection.length-1 : index,
        index = (index == this.collection.length) ? 0 : index;

    this.swapQuestions(this.collection.at(index));
  },

  swapQuestions : function(changed_model) {
    this.question.show( new QuestionView({model : changed_model}) );
  }
})

//
//-- U T I L S
//

function showPreviousScore() {
     if(user_name != "Anonymous") {
       FB.api('/' + fb_id + '/scores',function(response) {
         if(response.data.length) {
           old_score = response.data[0].score;
           userview.render({'name':user_name,'profile_pic':profile_pic,'score':response.data[0].score});
           console.log(JSON.stringify(response));
         } else {
           old_score = 0;
         }
       });
     }
}

function levelInfo() {
lin  = new LevelView();
lin.render({'level':level_name[playing_level],'num_quests':numQuestions,'correct_quests':numCorrect,'score':score,'num_try':numTry,'max_tries':MAXMARKINGS});
}

function selectCategory() {
  App.start();
   
}
function updateScore(score) {
  if( user_name != "Anonymous") {
    
    FB.api('/me/scores','post',{'score':score},function(response) {
      console.log(JSON.stringify(response));
    });
  }
}

function updateLevel(level) {
  $.ajax({ url:'/api/v1/updatelevel',
    type:'GET',
    data:{'level':level},
    success:function(data) {
      console.log("Level Updated !!!");
    }
  });
}
 
function updateAchievement(new_achievement) {
  if(user_name != "Anonymous") {
    $.ajax({url:'/api/v1/updateachievement',
            type:'GET',
            data:{'achieved':new_achievement},
            success:function(data) {
              console.log(JSON.stringify(data));
            }
    });
  }
}

function gameOver(choice) {
  var achieved = 0 ,                          //-- is there a achievement ?
      newscore = 0,                           // -- is there a new score ?
      statusline = "";
                                              //-- Number of questions got correctly marked updated
  if(choice.get('correct') == 1) {
    score  = score + 3;                       //-- +3 for correct 
    numCorrect++;
    Mousetrap.trigger('down');                //-- shows next question
  } else {
    score = score - 1;                        //-- -1 from a wrong attempt
  }
  
  
  numTry++;                                   //-- updates number of tries
  
  
  levelInfo();                                //-- updates level information

  
  if(numCorrect == numQuestions) {            //-- game ends when all questions correctly answered
    
    
    if(numTry <= MAXMARKINGS ) {              //-- if the level is passed
 
      if(playing_level == last_unlocked_level){
        achieved = 1;
                                              //-- code for updating the user level, 
        
        score = score + 10 * playing_level;   //-- A bonus is given for  passing a level
        updateLevel(playing_level + 1);       //-- player level is updated in the database
        updateAchievement(playing_level);     //-- achievement posted in the players timeline (if loggedin).
      } else {
                                              //-- code for showong play next game
      }
    } else {
      alert('Good Play, Need to imporve !!!');
    }
 
    if (score > old_score) {       //-- score need only be published if its new high score
      updateScore(score);
      newscore = 1;
    } 
    if(achieved == 1) {
    statusline = statusline + "Congratulations!!! you have Unlocked new level " + level_name[playing_level + 1] + "<br/>";
    }
    if(newscore == 1) {
      statusline = statusline + "You you have achieved a new high score - " + score + "<br/>";
    }
    statusline = statusline + "<a href='/play'> Play Again </a>";
    $('#content').html(statusline);
 }
}
  
//
//-- A P P  I N I T
//
var App = new Backbone.Marionette.Application(),
    questions = new QuestionCollection({}),
    gameview = null,
    numQuestions = 0,
    numCorrect = 0,
    MAXMARKINGS = 80,          //-- Maximum number of tries that user can try for passing a level. if numtry>80 level is not passed
    level_name= {1:'canser',2:'immunology',3:'metabolism',4:'kineases',5:'proteases'},
    profile_pic = $.cookie('profile_pic'),
    playing_level = 0,
    numTry = 0,
    score = 0,
    old_score = 0;


//-- Displays User Information
userview = new UserView();
userview.render({'name':user_name,'profile_pic':profile_pic,'score':-1});


App.addRegions({
  main : '#content'
});

App.addInitializer(function() {
    
    questions.fetch({async : false});


                                        //-- Generating Questions based on Levels
                                        //-- At present level 1 ==> Category 1 ,level 2 ==> Category 2 etc.
                                        //-- This area can be modified to add specific questions selection 
                                        //-- criteria later    
   
    cat_id = parseInt($('#cselect').val());
    
                                        //-- Set the current Playing level
    playing_level = cat_id
    
    $('#select-category').hide();
    qc = new QuestionCollection();
    quests = questions.filter(function(q) {
      if( q.get('categories').indexOf(cat_id) != -1 ) {qc.add(q);return true;}
      else return false;
    });

                                 
    numQuestions = qc.length;           //-- number of questions
    MAXMARKINGS = numQuestions * 2;     //-- a average of two tries per questions
    gameview = new GameView({collection:qc});
    showPreviousScore();                //-- displays previous max score
    

    levelInfo();                        //-- Displays the level information
    App.main.show( gameview  );         //-- initializes the games
  
});
  

                                        //-- Javascript Facebook
                                        //-- For Authentication
  window.fbAsyncInit = function() {
    //--  init the FB JS SDK
    FB.init({
      appId      : '159866620823022',
      status     : true,
      xfbml      : true
    });
    
};

(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/all.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));



