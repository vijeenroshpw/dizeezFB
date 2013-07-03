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
  idAttribute:'disease_id'
  defaults : {
    disease_id    : -1,
    disease_name  : ""
  },
});

//
//-- Views
//
var QuestionView = Backbone.View.extend({
    //-- This is the qustion view which ... (please detail out here)
    el : '#question',
    //-- This is a great start, but these long strings are hard and difficult to read. Take a look at
    //-- this SO post: http://stackoverflow.com/questions/4912586/explanation-of-script-type-text-template-script 
    //-- and check out the images that I sent Karthik on Jun 26th in HipChat. Putting templates into a script
    //-- tag will save you headaches and time in the long run!
    template : "<from name='questions'><table class = 'table table-hover'> <thead><tr><th><%= clue_name %></th></tr></thead><tbody><tr><th id=option0> <input  type=radio value=0 name=answer class='opt' > <%= opt0 %> </th></tr><tr><th id=option1> <input  type=radio value=1 name=answer class='opt' > <%= opt1 %></th></tr><tr><th id=option2> <input  type=radio value=2 name=answer class='opt' > <%= opt2 %> </th></tr><tr><th id=option3> <input  type=radio value=3 name=answer class='opt' > <%= opt3 %> </th></tr><tr><th id=option4> <input  type=radio value=4 name=answer class='opt' > <%= opt4 %> </th></tr></tbody></table></form> ",
    events : {
      'click .opt': 'nextQuestion'
    },
    nextQuestion : function() {
      if(this.isTrue()) {
        DIZEEZ_FB.score += 10;
        //-- Is there a better way to handle updating the DOM than using a global jQuery selector in here?
        //-- Perhaps the div#score element should be handled by a view? Are you familar with this.$el? It's
        //-- a way that you can access the jquery object for the current view you're in.
        $('#score').html("SCORE:" + DIZEEZ_FB.score);
      }
      DIZEEZ_FB.quest_number++;
      this.render(DIZEEZ_FB.questcoll.at(DIZEEZ_FB.quest_number));
    },
    render : function(model) {
      model.addOptNames();
      var compiledTemplate = _.template(this.template, model.toJSON());
      this.$el.html(compiledTemplate);
    },
    isTrue : function() {
      var $question = $('input[name="answer"]:checked');
      if ( parseInt($question.val()) == DIZEEZ_FB.questcoll.at(DIZEEZ_FB.quest_number).get('correct_index') ) {
        return true
      } else {
        return false;
      }
    });

//
//-- Collections
//
var QuestCollection = Backbone.Collection.extend({
  model : Question,
  //-- Let's add an api namespace here so it's more version friendly. Example: /api/v1/questions
  url : '/questions',
});

var DiseasesCollection = Backbone.Collection.extend({
  model:Diseases,
  url:'/diseases'
});

//
//-- App Init!
//
var DIZEEZ_FB = {};

DIZEEZ_FB.quest_number = 0;
DIZEEZ_FB.score = 0;
DIZEEZ_FB.time = 60;
DIZEEZ_FB.question_view = new QuestionView();
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
