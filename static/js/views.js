var QuestionView = Backbone.View.extend({
			el:'#question',
			render:function(options,model) {
				var template = "<from name='questions'><table class = 'table table-hover'> <thead><tr><th><%= clue_name %></th></tr></thead><tbody><tr><th id=option0> <input  type=radio value=0 name=answer onclick='nextQuestion()'> <%= opt0 %> </th></tr><tr><th id=option1> <input  type=radio value=1 name=answer onclick='nextQuestion()'> <%= opt1 %></th></tr><tr><th id=option2> <input  type=radio value=2 name=answer onclick='nextQuestion()'> <%= opt2 %> </th></tr><tr><th id=option3> <input  type=radio value=3 name=answer onclick='nextQuestion()'> <%= opt3 %> </th></tr><tr><th id=option4> <input  type=radio value=4 name=answer onclick='nextQuestion()'> <%= opt4 %> </th></tr></tbody></table></form> "; 
				options['clue_name'] = model.get('clue_name');
				var compiledTemplate = _.template(template,options);
				this.$el.html(compiledTemplate);
			}
		   });



