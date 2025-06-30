# Development Notes

## My Approach to Building This Recommendation Engine

### Initial Planning (Day 1)
- Spent time understanding the requirements and sketching out the architecture
- Decided to use FastAPI instead of Flask for better async support and automatic documentation
- Chose to implement a robust fallback system in case the LLM API fails

### Key Challenges Faced

#### 1. Prompt Engineering
The biggest challenge was getting consistent JSON responses from the LLM. I went through several iterations:
- **First attempt**: Simple prompt asking for recommendations
- **Problem**: Inconsistent response format, sometimes got plain text instead of JSON
- **Solution**: Very explicit JSON schema in the prompt with examples

#### 2. Token Optimization
Initially was hitting token limits with large product catalogs:
- **Solution**: Implemented product filtering to only send relevant products to the LLM
- **Optimization**: Reduced prompt verbosity while maintaining clarity

#### 3. Frontend State Management
Managing the flow between preferences, browsing history, and recommendations:
- **Challenge**: Keeping all states in sync across components
- **Solution**: Centralized state management in App.js with proper prop drilling

### Technical Decisions

#### Why OpenRouter + Gemini instead of OpenAI?
- **Cost**: Significantly cheaper for experimentation
- **Quality**: Gemini 2.0 Flash performs comparably to GPT-3.5-turbo for this use case
- **Requirements**: Assignment says "or similar" so this meets the criteria

#### Why FastAPI over Flask?
- **Documentation**: Auto-generated API docs with Swagger
- **Performance**: Better async handling for LLM API calls
- **Type Safety**: Pydantic models for request/response validation

#### Fallback Strategy
Implemented intelligent fallback recommendations when LLM API fails:
- **Rule-based**: Uses preference matching and product ratings
- **Graceful**: Users still get recommendations even during API issues
- **Transparent**: Clear indication when fallback is used

### Areas for Improvement

If I had more time, I would add:
1. **Caching**: Redis cache for LLM responses to reduce costs
2. **A/B Testing**: Different prompt strategies for optimization
3. **User Persistence**: Save preferences and history across sessions
4. **Better Error Handling**: More granular error states and user feedback
5. **Performance**: Pagination for large catalogs, lazy loading images

### Lessons Learned

- **Prompt Engineering is an Art**: Took multiple iterations to get reliable results
- **Fallback Systems Matter**: Users expect the app to work even when APIs fail
- **State Management Complexity**: React state gets complex quickly with multiple data flows
- **API Design**: Good error handling and response structure saves debugging time later

### Time Breakdown

- **Backend API & LLM Integration**: ~6 hours
- **Prompt Engineering & Testing**: ~4 hours  
- **Frontend Components**: ~8 hours
- **Styling & UX Polish**: ~3 hours
- **Integration & Testing**: ~3 hours
- **Documentation**: ~2 hours

**Total**: ~26 hours over 4 days

### Final Thoughts

This was a great learning experience, especially around prompt engineering and handling LLM responses reliably. The fallback system ended up being crucial during development when I hit API limits. Overall happy with the balance between functionality and code quality.
