//
// M O D E L S
//

//-- Question Model
var Question = Backbone.RelationalModel.extend({
  defaults : {
    id    : -1,
    text  : "",
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

//-- Choice Model
var Choice = Backbone.RelationalModel.extend({
  defaults: {
    choice_id : -1,
    correct   : 0,
    text      : ""
  },
});

//
// C O L L E C T I O N S
//
var ChoiceCollection = Backbone.Collection.extend({
  model:Choice
});

var QuestionCollection = Backbone.Collection.extend({
  model:Question,
  url:"/api/v1/questions"
});

//
// V I E W S
//
var ChoiceView = Backbone.View.extend({
  el:'#choices-area',
  render:function(model) {
    var compiledTemplate = _.template($('#choice-template').html(),model.toJSON());
    this.$el.append(compiledTemplate);
  },
});

var QuestionView = Backbone.View.extend({
  el:'#question-area',
  render:function(model) {
    //-- renders the question text
    compiledTemplate=_.template($('#question-template').html(),model.toJSON());
    this.$el.html(compiledTemplate);
    choice = new ChoiceView();
    //-- renders the choices
    for(i = 0;i<model.get('choices').length;i++)
      choice.render(model.get('choices').at(i));
  }
});

var DIZEEZ_FB = {};
DIZEEZ_FB.quests = new QuestionCollection({});
DIZEEZ_FB.quests.fetch({async:false});            //-- replace with the callback 
DIZEEZ_FB.questview = new QuestionView();
DIZEEZ_FB.questNum = 0;
DIZEEZ_FB.score = 0;
DIZEEZ_FB.totalQuestions = DIZEEZ_FB.quests.length;
DIZEEZ_FB.timerHandle = null;
DIZEEZ_FB.responseTime = 0;                      //-- keeps track of lag between answering
DIZEEZ_FB.timerFunction = function() {
  DIZEEZ_FB.responseTime++;
}

DIZEEZ_FB.start = function() {
  //-- initalize the timer ( for measuring the response time
  DIZEEZ_FB.timerHandle = window.setInterval(DIZEEZ_FB.timerFunction,1000);

  //-- display the first question
  DIZEEZ_FB.questview.render(DIZEEZ_FB.quests.at(DIZEEZ_FB.questNum));

}

DIZEEZ_FB.displayNextQuestion = function() {

  //-- Was the clicked answer true ?
  var $answer = $('input[name="choice"]:checked');
  if (parseInt($answer.val()) == 1){
    alert('Correct !!! ,  Response Time = '+ DIZEEZ_FB.responseTime);
    //--TODO update score here
  }

  //-- TODO update log model here
  //-- log will be a model , which will be updated after each question , finaly persisted to server at end of game 

  //-- Clear the previous question's text and choices 
  $('#question-area').empty()
  $('#choices-area').empty()

  // display next question  ramp up in case questions end TODO: ramp from a random question 
  DIZEEZ_FB.questNum = (DIZEEZ_FB.questNum + 1) % DIZEEZ_FB.totalQuestions;
  DIZEEZ_FB.questview.render(DIZEEZ_FB.quests.at(DIZEEZ_FB.questNum));  

  // reset response tim 
  DIZEEZ_FB.responseTime = 0;
}

DIZEEZ_FB.end = function() {
  console.log(" Log written succesfully \n");
}
