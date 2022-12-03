import React, {useState, useEffect} from 'react'

function App(){
  const [data, setData] = useState([{}])
  useEffect(()=>{
    fetch("/manage/accounts").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])
  return(
<div>
  {(typeof(data.all_blocked) === 0) ? (
    <p>Loading...</p>
  ) : (
    <p>
      {/* {data.total_acc_info[0].aid} */}
      오예 성공,, 이제 데이터를 어떤식으로 받아오고 렌더링해서 보여주는지, javascript의 객체 다루는 법 등.. 공부
    </p>
  )}
</div>
  )
}

export default App