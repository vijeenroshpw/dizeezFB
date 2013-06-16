// Question Model 
var Question = Backbone.Model.extend({
		defaults:{
			question_id:-1,
			clue_id:-1,
			clue_name:"",
			succes_rate:0,
			clue:"",
			answer:"",
			doid:"",
			choice_list:[],
			correct_index:0
		},
		idAttribute:'question_id'
	      });

// Question Collection
var QuestCollection = Backbone.Collection.extend({
				model:Question,
				url:'/questions'
				
			});

var Diseases = Backbone.Model.extend({
			defaults:{
				disease_id:-1,
				disease_name:""
			},
			idAttribute:'disease_id'
		});
var DiseasesCollection = Backbone.Collection.extend({
				model:Diseases,
				url:'/diseases'
			 });


