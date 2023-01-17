import React from "react";

export default function Profiles({ allValues }) {
    return (
        <div id="profile">
            {item(allValues)}
        </div>
    )
}

function item(data){
    return (
        <>
            {
                data.map((value, index) => (
                    <div className="flex">
                        <div className="item">
                            <img src={value.userAvatar} alt="" />

                            <div className="info">
                                <h3 className="name text-dark">{value.realName}</h3>
                                <span>Location</span>
                            </div>
                        </div>
                        <div className="item">
                            <span>{value.currentRating}</span>
                        </div>
                    </div>
                ))

            }
        </>
    )
}