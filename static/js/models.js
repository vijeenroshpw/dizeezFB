// Question Model 
var Question = Backbone.Model.extend({
		defaults:{
			question_id:-1,
			clue_id:-1,
			clue_name:"",
			succes_rate:0,
			clue:"",
			answer:"",
			doid:""
		},
		idAttribute:'question_id'
	      });

// Question Collection
var QuestCollection = Backbone.Collection.extend({
				model:Question,
				url:'/questions'
				
			});


