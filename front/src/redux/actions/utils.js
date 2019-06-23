export function makeCreators(type, ...argNames) {
    return function(...args) {
        const action = {
            type,
            payload: {}
        }
        argNames.forEach((argName, index) => {
            action.payload[argName] = args[index]
        })
        return action
    }
}