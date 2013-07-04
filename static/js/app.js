//
//-- Models
//
var Question = Backbone.Model.extend({
  idAttribute : 'question_id',
  defaults : {
    question_id   : -1,
    clue_id       : -1,
    clue_name     : "",
    succes_rate   : 0,
    clue          : "",
    answer        : "",
    doid          : "",
    choice_list   : [],
    correct_index : 0
  },
  addOptNames:function() {              //function depends on disnames being defined
    var cl = this.get('choice_list'),
        disname = DIZEEZ_FB.disname;

    this.set('opt0',disname[cl[0]-1]);
    this.set('opt1',disname[cl[1]-1]);
    this.set('opt2',disname[cl[2]-1]);
    this.set('opt3',disname[cl[3]-1]);
    this.set('opt4',disname[cl[4]-1]);
    return this;
  }
});

var Diseases = Backbone.Model.extend({
  idAttribute:'disease_id',
  defaults : {
    disease_id    : -1,
    disease_name  : ""
  },
});

//
//-- Views
//
var ScoreView = Backbone.View.extend({
    el:'div#score',
    initialize:function() {
      this.update(0);
    },
    update:function(current_score) {
      this.$el.html("SCORE : " + current_score);
    }
});		
var QuestionView = Backbone.View.extend({
    //-- This is the qustion view which will display questions . The view's render method , will take a 
    //-- question model instance , and display the question inside the div#question . The template is popu
    //-- lated with values from the question model instance.
    el : '#question',
    
    events : {
      'click .opt': 'nextQuestion'
    },
    nextQuestion : function() {
      if(this.isTrue()) {
        DIZEEZ_FB.score += 10;
        DIZEEZ_FB.scoreview.update(DIZEEZ_FB.score);
      }
      DIZEEZ_FB.quest_number++;
      this.render(DIZEEZ_FB.questcoll.at(DIZEEZ_FB.quest_number));
    },
    render : function(model) {
      model.addOptNames();
      var compiledTemplate = _.template($('#question-template').html(), model.toJSON());
      this.$el.html(compiledTemplate);
    },
    isTrue : function() {
      var $question = $('input[name="answer"]:checked');
      if ( parseInt($question.val()) == DIZEEZ_FB.questcoll.at(DIZEEZ_FB.quest_number).get('correct_index') ) {
        return true;
      } else {
        return false;
      }
    }
    });

//
//-- Collections
//
var QuestCollection = Backbone.Collection.extend({
  model : Question,
  //--  /api/v1/questions  A version friendly url 
  url : '/api/v1/questions',
});

var DiseasesCollection = Backbone.Collection.extend({
  model:Diseases,
  url:'/api/v1/diseases'
});

//
//-- App Init!
//
var DIZEEZ_FB = {};

DIZEEZ_FB.quest_number = 0;
DIZEEZ_FB.score = 0;
DIZEEZ_FB.time = 60;
DIZEEZ_FB.question_view = new QuestionView();
DIZEEZ_FB.scoreview = null;                  //-- will be populated by star() method
DIZEEZ_FB.timeHandle = null;
DIZEEZ_FB.timeUpdate = function() {
  if(DIZEEZ_FB.time <= 0) {
    alert("Time's Up Buddy !!!");
    window.clearInterval(DIZEEZ_FB.timeHandle);
  } else {
    DIZEEZ_FB.time--;
    $("#time").html("TIME:"+DIZEEZ_FB.time);
  }
}

DIZEEZ_FB.start = function() {
  DIZEEZ_FB.timeHandle = window.setInterval(DIZEEZ_FB.timeUpdate,1000); 
  DIZEEZ_FB.scoreview = new ScoreView();
  DIZEEZ_FB.question_view.render(DIZEEZ_FB.questcoll.at(DIZEEZ_FB.quest_number));
}

DIZEEZ_FB.end = function() {
  DIZEEZ_FB.time = 60;
  DIZEEZ_FB.score = 0;
}

DIZEEZ_FB.discoll = new DiseasesCollection({});
DIZEEZ_FB.questcoll = new QuestCollection({});
DIZEEZ_FB.questcoll.fetch({async:false}); // TODO Convert to Callback
DIZEEZ_FB.discoll.fetch({async:false});   // TODO Convert to Callback
DIZEEZ_FB.disname = DIZEEZ_FB.discoll.pluck('disease_name');
