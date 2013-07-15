// Code here need to be moved to  app.js file 
		
//
// M O D E L S
//
		
//-- Question Model
var Question = Backbone.RelationalModel.extend({
  defaults : {
    id : -1,
    text:"",
    choices:[]	
  },

  relations: [{
    type: Backbone.HasMany,
    key: 'choices',
    relatedModel: 'Choice',
    collectionType: 'ChoiceCollection',
    reverseRelation: {
      key: 'question',
      includeInJSON: 'id'
			// 'relatedModel' is automatically set to 'Zoo'; the 'relationType' to 'HasOne'.
    }
  }]
});

//-- Choice Model
var Choice = Backbone.RelationalModel.extend({
  defaults: {
    choice_id:-1,
    correct:0,
    text:""
  },
});
	      
	      
//
// C O L L E C T I O N S
//
	    
//-- Choice Collection
var ChoiceCollection = Backbone.Collection.extend({
  model:Choice
});
   
//-- Question Collection
              
var QuestionCollection = Backbone.Collection.extend({
  model:Question,
  url:"/api/v1/questions"
});


//
// V I E W S
//
  
//-- Choice view
var ChoiceView = Backbone.View.extend({
  el:'#choices-area',
  render:function(model) {
    var compiledTemplate = _.template($('#choice-template').html(),model.toJSON());
    this.$el.append(compiledTemplate);
  },
});
       
//-- Question View 
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
DIZEEZ_FB.inst_id = 0;
DIZEEZ_FB.displayNextQuestion = function() {
  //-- first clear previous question tag, choices
  var $answer = $('input[name="choice"]:checked');
  if (parseInt($answer.val()) == 1){
    alert('score awarded');
    //--TODO update score here
  }
       
  //-- TODO update log model here
  //-- log will be a model , which will be updated after each question , finaly persisted to server at end of game 
 
  $('#question-area').empty()
  $('#choices-area').empty()
                  
  // fetch next question
  DIZEEZ_FB.questNum++;
  DIZEEZ_FB.questview.render(DIZEEZ_FB.quests.at(DIZEEZ_FB.questNum));  
}                  
DIZEEZ_FB.questview.render(DIZEEZ_FB.quests.at(DIZEEZ_FB.questNum));  


