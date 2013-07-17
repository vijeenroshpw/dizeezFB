//
//-- M O D E L S
//
var Question = Backbone.RelationalModel.extend({
  defaults : {
    text  : '',

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

var GameView = Backbone.Marionette.Layout.extend({
  template : '#game-template',

  regions : {
    question  : '.game.question',
    list      : '.game.list ol'
  },

  initialize : function(options) {
    this.collection.bind('change:active', this.swapQuestions, this);
  },

  onRender : function() {
    var self = this;
    this.question.show( new QuestionView({model : this.collection.at(0)}) );
    this.list.show( new QuestionCollectionView(this.options) );

    Mousetrap.bind(['up', 'right'], function() { self.loop(1); });
    Mousetrap.bind(['down', 'left'], function() { self.loop(-1); })
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
//-- A P P  I N I T
//
var App = new Backbone.Marionette.Application(),
    questions = new QuestionCollection({});

App.addRegions({
  main : '#content'
});

App.addInitializer(function() {
  questions.fetch({async : false});
  //-- A "game" is defined by a collection of questions
  App.main.show( new GameView({collection: questions}) );
});

App.start();
