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
  render:function() {
    compiledTemplate = _.template(this.template,this.model.toJSON());
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
    Mousetrap.trigger('down');
    this.model.get('parentQuestion').set('answered', true);
    this.model.save({'active' : true});
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
    this.score.show( new ScoreView({collection : new ChoiceCollection(_.flatten(_.map(self.collection.pluck('choices'), function(collection) { return collection.models }))) }) );

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
function selectCategory() {
  App.start();
   
}

//
//-- A P P  I N I T
//
var App = new Backbone.Marionette.Application(),
    questions = new QuestionCollection({}),
    gameview = null,
    start = null,
    user = null,
    fb_id = "xxxxxxxxxx",
    user_name = "Anonymous",
    profile_pic = "",
    user_view = null;

App.addRegions({
  main : '#content'
});

App.addInitializer(function() {
    start = function() {
    questions.fetch({async : false});
    //Filter 1

    //Filter 2

    //Finaly applying user selected category
    cat_id = parseInt($('#cselect').val());
    $('#select-category').hide();
    qc = new QuestionCollection();
    quests = questions.filter(function(q) {
      if( q.get('categories').indexOf(cat_id) != -1 ) {qc.add(q);return true;}
      else return false;
    });
    //console.log(JSON.stringify(qc)); 
    gameview = new GameView({collection:qc});
    
  
    App.main.show( gameview  );
  }
  user = new User({'id':fb_id,'name':user_name});
  //-- fetches and sets profile pic 
  //-- any code that does the ui population relating to FB content will go here
  FB.api('/me/picture',function(response) {
          //profile_pic = response.data.url;
          // -- Anonymous.jpg is NOT an anonymous user symbol, please find a better one
          profile_pic = (response.data)?response.data.url:"/img/Anonymous.jpg";
          user.set({'profile_pic':profile_pic});
          user_view = new UserView({'model':user});
          user_view.render();
  });
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

  //-- Clears cookie
  $.cookie('api_key','');

  //-- Facebook Login
  FB.login(function(response) {
    if (response.authResponse) {
      console.log('Welcome!  Fetching your information.... ');
      //-- Fetches user information
      FB.api('/me', function(response) {
        user_name = response.name;                        //sets the username
        fb_id =  response.id;                             // sets FB ID
        //App.start();
      });
    } else {
      console.log('User cancelled login or did not fully authorize.');
      //App.start();                   //starts the application here
    }
  });
};

(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/all.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));
